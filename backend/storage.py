from pathlib import Path
import duckdb

SCHEMA = '''
CREATE TABLE IF NOT EXISTS bars_1m(symbol VARCHAR, ts TIMESTAMP, open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE, volume DOUBLE, amount DOUBLE, source VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS bars_1d(symbol VARCHAR, trade_date DATE, open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE, volume DOUBLE, amount DOUBLE, adjustment VARCHAR, source VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS emotion_daily(trade_date DATE, breadth DOUBLE, limit_up INTEGER, limit_down INTEGER, broken_board_rate DOUBLE, max_height INTEGER, promotion_rate DOUBLE, turnover_ratio DOUBLE, score DOUBLE, regime VARCHAR, previous_regime VARCHAR, transition VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS signals(symbol VARCHAR, ts TIMESTAMP, timeframe VARCHAR, signal VARCHAR, score DOUBLE, reason VARCHAR, strategy_version VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS intraday_states(symbol VARCHAR, ts TIMESTAMP, state VARCHAR, score DOUBLE, reason VARCHAR, source VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS board_ladder(trade_date DATE, symbol VARCHAR, name VARCHAR, board_height INTEGER, is_broken BOOLEAN, promoted BOOLEAN, theme VARCHAR, source VARCHAR, asof TIMESTAMP);
CREATE TABLE IF NOT EXISTS limit_up_pool(trade_date DATE, symbol VARCHAR, name VARCHAR, limit_time TIMESTAMP, first_limit_time TIMESTAMP, open_count INTEGER, seal_ratio DOUBLE, board_height INTEGER, theme VARCHAR, source VARCHAR, asof TIMESTAMP);
'''
def init_db(path='data/market.duckdb'):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(path) as con:
        con.execute(SCHEMA)
        for col, typ in [('promotion_rate','DOUBLE'),('previous_regime','VARCHAR'),('transition','VARCHAR')]:
            try: con.execute(f'ALTER TABLE emotion_daily ADD COLUMN {col} {typ}')
            except Exception: pass
        return con.execute("select current_timestamp as initialized_at").fetchone()[0]
