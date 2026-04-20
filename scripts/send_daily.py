#!/usr/bin/env python3
"""
上海美食日报推送脚本
每天 07:00 (北京时间) 执行
"""

import os
import requests
import random
from datetime import datetime

# 飞书 Webhook
WEBHOOK = os.environ.get("FEISHU_WEBHOOK")
if not WEBHOOK:
    WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/83044ef5-3b86-4d5e-a0c8-426043bc4205"

def get_day_of_week():
    """获取今天是周几 (北京时间)"""
    import pytz
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).weekday()

# 8个主题内容库
themes = {
    0: {  # 周一 - 怀旧情怀
        "name": "怀旧情怀",
        "items": [
            {"title": "过去进行食", "desc": "藏在弄堂里的老字号，味道几十年如一日", "location": "进贤路120号"},
            {"title": "威海路馄饨", "desc": "皮薄馅大，汤鲜到心坎里", "location": "威海路860号"},
            {"title": "老大昌", "desc": "老上海西点，奶油蛋糕还是那个味", "location": "淮海中路766号"},
            {"title": "又一村", "desc": "汤团界的扛把子，芝麻汤团一绝", "location": "四牌楼路20号"}
        ]
    },
    1: {  # 周二 - 潮人打卡
        "name": "潮人打卡",
        "items": [
            {"title": "安福路", "desc": "咖啡店扎堆，帅哥美女出没地", "location": "徐汇区安福路"},
            {"title": "今潮8弄", "desc": "弄堂美学新地标，拍照超出片", "location": "虹口区四川北路"},
            {"title": "徐汇滨江", "desc": "江边骑行+咖啡，惬意下午茶", "location": "徐汇区龙腾大道"},
            {"title": "1933老场坊", "desc": "工业风建筑，ins风满满", "location": "虹口区溧阳路611号"}
        ]
    },
    2: {  # 周三 - 老字号
        "name": "老字号",
        "items": [
            {"title": "国际饭店蝴蝶酥", "desc": "排队2小时也要买，香脆到停不下来", "location": "黄河路112号"},
            {"title": "四如春冷面", "desc": "上海冷面鼻祖，夏日必吃", "location": "石门一路56号"},
            {"title": "大壶春生煎", "desc": "清水生煎开创者，皮薄汁多", "location": "福建中路90号"},
            {"title": "鲜得来", "desc": "排骨年糕老牌子，酱汁一绝", "location": "云南南路28号"}
        ]
    },
    3: {  # 周四 - 苍蝇小馆
        "name": "苍蝇小馆",
        "items": [
            {"title": "玖玖小炒", "desc": "居民楼下的隐藏美味，本帮菜绝了", "location": "进贤路128号"},
            {"title": "进贤路本帮", "desc": "老弄堂里的本帮味道，人均50吃撑", "location": "进贤路56号"},
            {"title": "阿大葱油饼", "desc": "老手艺葱油饼，酥脆香到爆炸", "location": "茂名南路159号"}
        ]
    },
    4: {  # 周五 - 咖啡甜品
        "name": "咖啡甜品",
        "items": [
            {"title": "Arabica%", "desc": "咖啡届网红，杯子设计感满分", "location": "武康路368号"},
            {"title": "巨鹿路咖啡街", "desc": "整条街都是咖啡店，选择困难症犯了", "location": "静安区巨鹿路"},
            {"title": "WIYF", "desc": "冰淇淋界天花板，排队也值得", "location": "武康路202号"}
        ]
    },
    5: {  # 周六 - 夜市美食
        "name": "夜市美食",
        "items": [
            {"title": "昌里路夜市", "desc": "曾经的夜市王者，黑暗料理聚集地", "location": "昌里路历城路交叉口"},
            {"title": "寿宁路小龙虾", "desc": "夏天必吃，麻辣十三香全安排", "location": "寿宁路"},
            {"title": "定西路烧烤", "desc": "深夜食堂，撸串喝酒好去处", "location": "定西路"}
        ]
    },
    6: {  # 周日 - 周末探店
        "name": "周末探店",
        "items": [
            {"title": "思南公馆", "desc": "洋房里的brunch，格调满分", "location": "思南路51号"},
            {"title": "M50创意园", "desc": "艺术仓库改造，文艺青年必去", "location": "莫干山路50号"},
            {"title": "愚园路漫步", "desc": "梧桐树下老洋房，Citywalk路线推荐", "location": "静安区愚园路"}
        ]
    }
}

def generate_daily_content():
    """生成每日美食日报"""
    day = get_day_of_week()
    theme = themes[day]
    items = theme["items"]

    # 随机选择4-5个推荐
    selected = random.sample(items, min(5, len(items)))

    header = f"""🥢 上海美食日报
━━━━━━━━━━━━━━━━━━━━
📅 {datetime.now().strftime('%Y年%m月%d日 %A')}
🏷️ 今日主题：{theme['name']}
━━━━━━━━━━━━━━━━━━━━

"""

    body = ""
    for i, item in enumerate(selected, 1):
        body += f"{i}. 【{item['title']}】\n   {item['desc']}\n   📍 {item['location']}\n\n"

    footer = """━━━━━━━━━━━━━━━━━━━━
💬 你们今天吃什么了？
评论区分享给我呀～

收藏起来，周末打卡去！"""

    return header + body + footer

def send_to_feishu(content):
    """发送到飞书"""
    url = WEBHOOK
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }

    response = requests.post(url, json=payload)
    result = response.json()

    if result.get("code") == 0:
        print("✅ 飞书消息发送成功")
        return True
    else:
        print(f"❌ 发送失败: {result}")
        return False

if __name__ == "__main__":
    print(f"📅 当前日期: {datetime.now().strftime('%Y-%m-%d')}")

    content = generate_daily_content()
    print(f"\n📝 生成内容:\n{content}")

    send_to_feishu(content)
