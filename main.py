"""
main8days.py - 8 天压缩版项目主入口
====================================
"""
from src.dp01 import load_data_native, analyze_by_category_native
from src.dp02 import fill_weather_to_csv

def task01():
    print("===================")
    print("任务1：统计csv订单数据")
    print("===================")
    orders = load_data_native()
    result = analyze_by_category_native(orders)
    n = len(orders)
    total = 0
    for o in orders:
        try:
            t = float(o["amount"])
        except:
            t = 0
        total = total + t

    print(f"订单数据共{n}条，总金额:{total:,.2f}元")
    print("其中：")
    for cat,dc in result.items():
        print(f"{'未知' if cat=='' else cat}类订单共{dc['count']}条，合计金额：{dc['total']:,.2f}元")

def task02():
    print("===================")
    print("任务2：订单数据添加天气气温")
    print("===================")
    fill_weather_to_csv()
    print("任务2完成")

def main():
    print('=' * 50)
    print('电商订单分析 ')
    print('=' * 50)
    task01()
    task02()


if __name__ == '__main__':
    main()
