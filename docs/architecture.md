# A股量化系统设计（深度方案）

## 1. 上游 API 接入边界
上游仓库当前将能力分为：标的检索/消歧、实时快照、历史价格、财务报表、指数与板块、涨停/特色数据，并同时提供 REST、Python toolkit、CLI、MCP。系统统一使用 REST adapter，`X-api-key` 只在服务端注入。接入顺序：
1. ticker search：名称/代码不完整时绝不猜交易所后缀；缓存 `thscode` 与证券状态。
2. prices snapshot / history：原始层保留复权口径、窗口、抓取时间与上游响应哈希。
3. index/sector/limit-up：生成市场宽度、题材扩散、涨停梯队和情绪 regime。
4. financials：按报告期建立 point-in-time 表，避免把后披露财务数据倒灌到历史回测。

限流、分页和大结果必须任务化落 DuckDB；线上契约以 `docs/api` 与 `/docs` 为准，不把示例字段当合同。

## 2. 数据模型
SQLite：`symbols`、`jobs`、`strategies`、`portfolios`、`risk_rules`、`audit_logs`。
DuckDB：`raw_*`（不可变）、`bars_1d`、`bars_1m`、`quotes_snapshot`、`factors`、`emotion_daily`、`signals`、`fills`、`equity_curve`。所有表带 `trade_date/asof/source/adjustment`；交易日历、停牌、ST、上市天数、涨跌停价单独维护。

## 3. 分时语言：不是把 1 分钟 K 线当成日线缩小版
分时状态机每 1 分钟更新：
- **位置**：`p_rel=(price-prev_close)/(limit_up-prev_close)`，距 VWAP、开盘价、日内高低点的 z-score。
- **节奏**：价格斜率、VWAP 斜率、连续创新高/低、回撤恢复时间；开盘 09:30-09:35、午后 13:00-13:10 分开建模。
- **量能**：`volume / 同时段历史中位量`（不能用当日未来成交量）；主动买卖量、量价背离、放量突破与缩量回踩。
- **结构**：开盘缺口、首小时强弱、均价线承接、冲高回落、尾盘抢筹；集合竞价单独建模，不能和连续竞价混合。
- **约束**：停牌、涨跌停、T+1、最小交易单位、可卖数量；封板要看封单稳定性与炸板次数，不把“触及涨停”当成“封死”。

状态示例：`OPENING_DISCOVERY → TREND_ABOVE_VWAP → PULLBACK_SUPPORT → BREAKOUT_CONFIRM`，风险状态：`VWAP_LOSS → DISTRIBUTION → LIMIT_DOWN_RISK`。每个状态只产生候选信号，最终须经情绪、流动性、组合风控门控。

## 4. K线语言
K线层分三级：
- 单根：实体/上下影、缺口、收盘位置（CLV）、ATR 标准化振幅；只命名为形态特征，不直接等于买卖。
- 结构：HH/HL、LH/LL、突破-回踩、平台/箱体、缺口回补、趋势线；用 fractal 与 ATR 阈值消除噪声。
- 量价：OBV/AD、相对成交量、突破时量能、缩量回踩；信号必须要求指数/板块相对强度确认。
TA-Lib 适合批量计算 SMA/EMA、MACD、RSI、ADX、ATR、BBANDS、STOCH、OBV、MFI、CDL* 形态；CDL 只作为特征，不能单独交易。缺失值、预热窗口、参数版本全部写入因子元数据。

## 5. 情绪周期 regime
每日按市场/板块聚合：涨跌家数比、涨停数、跌停数、炸板率、连板最高高度、首板/晋级率、平均涨幅、成交额相对 20 日均值、指数趋势、强势股回撤。标准化后形成 `emotion_score`，但使用 HMM/阈值前必须 walk-forward 验证。
阶段：`冰点 → 修复 → 主升/高潮 → 分歧 → 退潮`。regime 是仓位上限与策略开关，不是预测标签：冰点只允许低仓试错，高潮禁止追高并提高止盈，退潮禁做高位接力。

## 6. 回测与风控
事件驱动撮合：停牌/涨跌停不可成交，买入 T+1，手续费/印花税/滑点可配置，集合竞价与连续竞价分开。按 as-of join 处理财务数据；先划分训练/验证/测试，再做滚动 walk-forward。输出 CAGR、年化波动、Sharpe、最大回撤、胜率、盈亏比、换手、容量、分 regime 归因。任何信号必须能追溯到因子值与数据快照。

## 7. 分阶段交付
MVP：数据 adapter + DuckDB schema + 日线/分时特征 + 情绪 dashboard。
V2：事件回测、组合优化、板块轮动、策略 DSL。
V3：实时 websocket/轮询、告警、纸上交易。实盘下单另行设计券商适配器、双人审批和 kill switch。
