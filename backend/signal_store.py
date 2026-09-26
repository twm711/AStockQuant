from datetime import datetime, timezone
import duckdb
from pathlib import Path

def save_signal(symbol, timeframe, result, path='data/market.duckdb'):
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 with duckdb.connect(path) as con:
  con.execute('CREATE TABLE IF NOT EXISTS signals(symbol VARCHAR, ts TIMESTAMP, timeframe VARCHAR, signal VARCHAR, score DOUBLE, reason VARCHAR, strategy_version VARCHAR, asof TIMESTAMP)')
  now=datetime.now(timezone.utc)
  con.execute('insert into signals values (?,?,?,?,?,?,?,?)',[symbol,now,timeframe,result['action'],result['score'],';'.join(result['reasons']),'baseline-v1',now])
 return now.isoformat()
