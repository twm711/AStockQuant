from datetime import datetime, timezone
from typing import Any

def envelope(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict): raise ValueError('响应必须是对象')
    if payload.get('code') not in (None, 0): raise ValueError(f"上游业务错误: {payload.get('code')} {payload.get('message','')}")
    return payload.get('data', payload)

def snapshots(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data=envelope(payload); items=data.get('item', []) if isinstance(data,dict) else []
    return [{**x, 'symbol':x.get('thscode'), 'price':x.get('last_price'), 'pct_chg':x.get('price_change_ratio_pct'), 'asof':datetime.now(timezone.utc).isoformat()} for x in items]

def daily_bars(payload: dict[str, Any], symbol: str, adjustment: str) -> list[dict[str, Any]]:
    data=envelope(payload); items=data.get('item', []) if isinstance(data,dict) else []
    return [{'symbol':symbol,'date_ms':x['date_ms'],'open':x['open_price'],'high':x['high_price'],'low':x['low_price'],'close':x['close_price'],'volume':x['volume'],'amount':x['turnover'],'adjustment':adjustment} for x in items]
