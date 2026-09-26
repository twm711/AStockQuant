# AStockQuant

A股量化研究与交易决策工作台（研究/回测优先，非投资建议）。

## 方案摘要
- **数据层**：同花顺 Fuyao REST 作为唯一远端事实源，API Key 仅从环境变量 `HITHINK_FINANCE_API_KEY` 读取；SQLite 保存配置、任务和策略版本，DuckDB 保存列式行情、因子与回测结果。
- **信号层**：TA-Lib（可选依赖）计算趋势、动量、波动率、量价指标；所有特征带 `asof` 时间戳，禁止未来数据泄漏。
- **A股语言**：分时是“价格位置 + 量能节奏 + 买卖盘/涨停约束”的状态机；K线是“结构 + 趋势 + 量价确认”的规则引擎；情绪周期是市场宽度、涨跌停、连板高度、炸板率、成交额和指数状态的综合 regime。
- **前端**：React + Ant Design + ECharts（当前提供可直接运行的静态 dashboard 原型）。

## 启动后端
```bash
cp .env.example .env
# 编辑 .env，填入你自己的 key（不要提交）
pip install -r requirements.txt
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

API：`/api/health`、`/api/capabilities`、`/api/market/snapshot`、`/api/analysis/{thscode}`、`/api/emotion/regime`。

## 前端
```bash
cd frontend && npm install && npm run dev
```

## 重要边界
接口契约以线上 `https://fuyao.aicubes.cn/docs/` 与上游仓库当前 `docs/api/` 为准；未知字段不猜测，先通过 ticker search 消歧。实盘交易、券商下单、风控审批尚未接入。
