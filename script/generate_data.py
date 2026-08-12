"""
scripts/generate_data.py
========================
生成 5000 条模拟电商订单数据（2023-01-01 至 2023-12-31）。

【教学设计】刻意混入：
  - 5% 的空值（amount / city / category 随机一字段置空）
  - 5% 的完全重复行
供 Day 4（异常与清洗）和 Day 6（Pandas dropna/drop_duplicates）使用。

运行方式：
  python scripts/generate_data.py
输出：
  data/raw_orders.csv
"""
import csv
import os
import random
from datetime import datetime, timedelta

# 固定随机种子，确保全班数据一致，便于对答案
random.seed(42)

CATEGORIES = ['Electronics', 'Clothing', 'Food', 'Books']
CITIES = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)
NUM_ORDERS = 5000
POLLUTION_RATIO = 0.05  # 5% 空值 + 5% 重复


def generate_one_order(i: int) -> dict:
    """生成第 i 条订单。"""
    span_days = (END_DATE - START_DATE).days
    return {
        'order_id': 100000 + i,
        'user_id': random.randint(1, 500),
        'order_date': (START_DATE + timedelta(days=random.randint(0, span_days))).strftime('%Y-%m-%d'),
        'category': random.choice(CATEGORIES),
        'amount': round(random.uniform(10, 2000), 2),
        'city': random.choice(CITIES),
    }


def generate_orders(n: int = NUM_ORDERS) -> list[dict]:
    """生成 n 条干净订单。"""
    return [generate_one_order(i) for i in range(n)]


def pollute(orders: list[dict], ratio: float = POLLUTION_RATIO) -> list[dict]:
    """
    故意污染数据：注入空值 + 复制重复行。

    对比 C 语言：相当于故意制造野指针/越界访问让学生用 valgrind 排查。
    """
    n = len(orders)
    # 1) 随机抽 ratio*n 行，置空其中一个字段
    nan_count = int(n * ratio)
    for _ in range(nan_count):
        idx = random.randint(0, n - 1)
        field = random.choice(['amount', 'city', 'category'])
        orders[idx][field] = ''  # CSV 中空字符串 = Pandas 读到的 NaN

    # 2) 复制 ratio*n 行作为重复
    dup_count = int(n * ratio)
    for _ in range(dup_count):
        orders.append(dict(random.choice(orders)))

    random.shuffle(orders)
    return orders


def save_csv(orders: list[dict], path: str = 'data/raw_orders.csv') -> None:
    """落盘为 CSV。自动创建目录。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)


def main() -> None:
    orders = generate_orders(NUM_ORDERS)
    orders = pollute(orders, POLLUTION_RATIO)
    save_csv(orders)
    print(f'[OK] 已生成 {len(orders)} 条订单（含污染）-> data/raw_orders.csv')


if __name__ == '__main__':
    main()
