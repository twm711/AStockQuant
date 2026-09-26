from typing import Any

def as_records(payload: Any):
    """Best-effort envelope unwrapping; preserves unknown fields for contract drift."""
    if isinstance(payload,list): return payload
    if not isinstance(payload,dict): return []
    for key in ('data','items','results','rows','list'):
        value=payload.get(key)
        if isinstance(value,list): return value
        if isinstance(value,dict):
            nested=as_records(value)
            if nested:return nested
    return [payload]
