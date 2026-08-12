import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']   # 中文
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('data/raw_orders.csv')
# df.head()
# df.info()
# 1. 类型转换
df['order_date'] = pd.to_datetime(df['order_date'])
# 2. 丢弃 amount 为空
df = df.dropna(subset=['amount'])
# 3. 去重
df = df.drop_duplicates(subset=['order_id'])
# 4. 填充 category
df['category'] = df['category'].fillna('未知')
# 验证
print(df.shape)
print(df.isnull().sum())
# df.head()
summary = df.groupby('category').agg(
    count=('order_id', 'count'),
    total=('amount', 'sum'),
    avg=('amount', 'mean'),
).sort_values('total', ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(summary.index, summary['total'], color='skyblue')
ax.set_xlabel('品类')
ax.set_ylabel('总销售额')
ax.set_title('各品类销售额对比')
plt.show()

# 1. 按日期聚合 + 排序
daily = df.groupby(df['order_date'].dt.date)['amount'].sum().reset_index()
daily.columns = ['date', 'total']
daily['date'] = pd.to_datetime(daily['date'])
daily['ma7'] = daily['total'].rolling(window=7).mean()
daily = daily.sort_values('date')

# 2. 画折线
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(daily['date'], daily['total'], color='steelblue', linewidth=1)
ax.plot(daily['date'], daily['ma7'], color='red', linewidth=2, label='7 日移动平均')
ax.set_title('每日销售额趋势（2023 年）')
ax.set_xlabel('日期'); ax.set_ylabel('销售额'); 
ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=df, x='amount', bins=30, kde=True, color='coral', ax=ax)
ax.set_title('订单金额分布'); ax.set_xlabel('金额'); ax.set_ylabel('订单数')
plt.tight_layout(); plt.show()