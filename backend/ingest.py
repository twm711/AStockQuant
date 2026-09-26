import json
from datetime import datetime, timezone
from pathlib import Path
import duckdb

def save_raw_snapshot(payload, codes, path='data/market.duckdb'):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with duckdb.connect(path) as con:
        con.execute('CREATE TABLE IF NOT EXISTS raw_snapshots (id BIGINT, fetched_at TIMESTAMP, symbols VARCHAR, payload JSON)')
        row=con.execute('select coalesce(max(id),0)+1 from raw_snapshots').fetchone()[0]
        con.execute('insert into raw_snapshots values (?,?,?,?)',[row,datetime.now(timezone.utc),','.join(codes),json.dumps(payload,ensure_ascii=False)])
    return row
