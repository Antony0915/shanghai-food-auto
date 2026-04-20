# 上海美食日报自动化

每天自动推送上海美食日报到飞书群。

## 功能

- 每天 07:00 (北京时间) 自动推送
- 8个主题轮换：怀旧情怀、潮人打卡、老字号、苍蝇小馆、咖啡甜品、夜市美食、周末探店、美食地图
- 每周7天内容完全不重复

## 配置

### 1. 设置 GitHub Secrets

在 GitHub 仓库 Settings → Secrets 中添加：

| Name | Value |
|------|-------|
| `FEISHU_WEBHOOK` | 飞书 Webhook URL |

### 2. 启用 Actions

在 GitHub 仓库 Actions 页面启用 workflow。

## 本地测试

```bash
pip install requests pytz
python scripts/send_daily.py
```
