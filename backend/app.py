from datetime import datetime, timezone
import os
from typing import Any
import httpx
from fastapi import FastAPI, HTTPException, Query
from pydantic_settings import BaseSettings, SettingsConfigDict
from .emotion import EmotionInput, score
from .storage import init_db
from .backtest import run as run_backtest, BacktestConfig
from .ingest import save_raw_snapshot
from .normalize import as_records
from .strategy import signal as strategy_signal
from .emotion_cycle import DayMetrics, classify as classify_cycle, transition as cycle_transition
from .risk import gate as risk_gate
from .signal_store import save_signal
from .attribution import by_regime
from .metrics import trade_metrics
from pydantic import BaseModel
import pandas as pd

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    hithink_finance_api_key: str = ''
    hithink_base_url: str = 'https://fuyao.aicubes.cn/api'

settings = Settings()
app = FastAPI(title='AStockQuant API', version='0.1.0')

@app.on_event('startup')
def startup():
    init_db(os.getenv('DUCKDB_PATH', 'data/market.duckdb'))

async def upstream(path: str, params: dict[str, Any]) -> Any:
    if not settings.hithink_finance_api_key:
        raise HTTPException(503, 'HITHINK_FINANCE_API_KEY 未配置')
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(settings.hithink_base_url.rstrip('/') + path,
            params=params, headers={'X-api-key': settings.hithink_finance_api_key})
    if r.status_code >= 400:
        raise HTTPException(r.status_code, f'上游接口错误: {r.text[:300]}')
    return r.json()

@app.get('/api/health')
def health():
    return {'status':'ok','time':datetime.now(timezone.utc).isoformat()}

@app.get('/api/dashboard/summary')
def dashboard_summary():
    # Single read model for the terminal; upstream-derived fields stay explicit.
    return {'market_status':'research','emotion':{'regime':'unknown','score':None},'breadth':None,'limit_up':None,'limit_down':None,'broken_board_rate':None,'max_height':None,'turnover_ratio':None,'source':'awaiting upstream emotion/limit-up sync'}

@app.get('/api/capabilities')
def capabilities():
    return {'domains':['a-share/symbol','a-share/prices','a-share/financials','a-share/index','a-share/sector','a-share/limit-up'],
            'upstream':'HiThink Fuyao REST; online contract is source of truth'}

@app.get('/api/market/snapshot')
async def snapshot(thscodes: str = Query(..., description='如 600519.SH，逗号分隔')):
    return await upstream('/a-share/prices/snapshot', {'thscodes': thscodes})

@app.post('/api/market/snapshot/sync')
async def sync_snapshot(thscodes: str = Query(...)):
    codes=[x.strip() for x in thscodes.split(',') if x.strip()]
    payload=await upstream('/a-share/prices/snapshot', {'thscodes': ','.join(codes)})
    row=save_raw_snapshot(payload,codes,os.getenv('DUCKDB_PATH','data/market.duckdb'))
    return {'snapshot_id':row,'symbols':codes,'records_seen':len(as_records(payload)),'stored':'raw_snapshots'}

@app.get('/api/market/history')
async def history(thscode: str, start: int, end: int, adjust: str = Query('forward', pattern='^(none|forward|backward)$')):
    if end <= start or end-start > 10*365*24*3600*1000: raise HTTPException(400, '时间窗口必须为正且不超过10年')
    return await upstream('/a-share/prices/historical', {'thscode':thscode,'interval':'1d','start':start,'end':end,'adjust':adjust})

class SignalRequest(BaseModel):
    close: float
    sma20: float
    rsi: float
    rel_volume: float
    above_vwap: bool
    regime: str

@app.post('/api/strategy/signal')
def strategy(req: SignalRequest, symbol: str = Query('UNKNOWN'), timeframe: str = Query('1d'), persist: bool = Query(False)):
    result = strategy_signal(**req.model_dump())
    if persist:
        result['stored_at'] = save_signal(symbol, timeframe, result, os.getenv('DUCKDB_PATH','data/market.duckdb'))
    return result

@app.get('/api/strategy/signals')
def signals(symbol: str | None = None, limit: int = Query(100, ge=1, le=1000)):
    import duckdb
    path=os.getenv('DUCKDB_PATH','data/market.duckdb')
    try:
        with duckdb.connect(path, read_only=True) as con:
            if symbol:
                rows=con.execute('select symbol,ts,timeframe,signal,score,reason,strategy_version,asof from signals where symbol=? order by ts desc limit ?', [symbol,limit]).fetchall()
            else:
                rows=con.execute('select symbol,ts,timeframe,signal,score,reason,strategy_version,asof from signals order by ts desc limit ?', [limit]).fetchall()
            cols=['symbol','ts','timeframe','signal','score','reason','strategy_version','asof']
            return [dict(zip(cols,r)) for r in rows]
    except Exception:
        return []

@app.get('/api/analysis/{thscode}')
async def analysis(thscode: str):
    # Orchestration boundary: fetch raw data first, then feature engine consumes it.
    data = await upstream('/a-share/prices/snapshot', {'thscodes': thscode})
    return {'thscode': thscode, 'data': data, 'features': {'status':'pending_history_window'},
            'methodology':'trend + momentum + volatility + volume confirmation; no look-ahead'}

class BacktestBar(BaseModel):
    date: str
    close: float
    signal: int = 0

@app.post('/api/backtest')
def backtest(bars: list[BacktestBar]):
    if len(bars) > 10000: raise HTTPException(413, '单次最多 10000 根K线')
    df=pd.DataFrame([x.model_dump() for x in bars])
    result=run_backtest(df)
    return {'metrics':{**result['metrics'],**trade_metrics(result['trades'])},'curve':result['curve'].to_dict(orient='records'),'trades':result['trades'],'attribution':by_regime(result['trades'])}

@app.get('/api/emotion/cycle')
def emotion_cycle(limit_up:int=Query(...,ge=0),limit_down:int=Query(...,ge=0),broken_rate:float=Query(...,ge=0,le=1),max_height:int=Query(...,ge=0),promotion_rate:float=Query(...,ge=0,le=1),breadth:float=Query(...,ge=0,le=1),turnover_ratio:float=Query(1,ge=0),previous:str|None=None):
    current=classify_cycle(DayMetrics(limit_up,limit_down,broken_rate,max_height,promotion_rate,breadth,turnover_ratio),previous)
    return {'regime':current,'previous_regime':previous,'transition':cycle_transition(previous,current),'inputs':{'limit_up':limit_up,'limit_down':limit_down,'broken_rate':broken_rate,'max_height':max_height,'promotion_rate':promotion_rate,'breadth':breadth,'turnover_ratio':turnover_ratio}}

@app.get('/api/risk/gate')
def get_risk_gate(regime: str = Query(...)):
    return risk_gate(regime)

@app.get('/api/emotion/regime')
async def emotion_regime(breadth: float = Query(.5, ge=0, le=1), limit_up: int = Query(0, ge=0), limit_down: int = Query(0, ge=0), broken_board_rate: float = Query(0, ge=0, le=1), max_height: int = Query(0, ge=0), turnover_ratio: float = Query(1, ge=0)):
    x=EmotionInput(breadth,limit_up,limit_down,broken_board_rate,max_height,turnover_ratio)
    value,regime=score(x)
    return {'regime':regime,'score':value,'inputs':x.__dict__,'method':'transparent baseline; walk-forward calibration required'}
