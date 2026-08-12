import pandas as pd

def train_model(daily, isDraw):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression

    X = daily[['avg_amount', 'temp']]   # 特征（2 列，注意双括号！）
    y = daily['sales']                  # 标签（1 列，Series 不是 DataFrame）

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,           # 20% 作测试
        random_state=42,         # 固定随机种子（保证全班结果一致）
    )

    print(f'训练集: {X_train.shape}, 测试集: {X_test.shape}')
    # 训练集: (292, 2), 测试集: (73, 2)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if isDraw:
        import matplotlib.pyplot as plt
        residuals = y_test - y_pred
        plt.scatter(y_pred, residuals)
        plt.axhline(0, color = 'red', linestyle='--')
        plt.xlabel('预测值')
        plt.ylabel('残差')
        plt.title('残差图')
        plt.show()
    return model


df = pd.read_csv('data/weather_orders.csv')
df['order_date'] = pd.to_datetime(df['order_date'])

# 按日期聚合
daily = df.groupby(df['order_date'].dt.date).agg(
    sales=('order_id', 'count'),         # 当天订单数（标签 y）
    avg_amount=('amount', 'mean'),       # 当天平均金额（特征 1）
    temp=('temp', 'mean'),               # 当天平均温度（特征 2）
).reset_index()

print(daily.head())


model = train_model(daily)
print(f'系数(coef):{model.coef_}')
print(f'截距(intercept):{model.intercept_}')



# 对比真实 vs 预测
result = pd.DataFrame({
    '真实': y_test.values,
    '预测': y_pred,
    '误差': y_test.values - y_pred,
})
print(result.head(10))

tomorrow = pd.DataFrame({'avg_amount':[1000], 'temp':[28]})
predicted_sales = model.predict(tomorrow)
print(f"预测明天订单数：{predicted_sales[0]:.0f}")

from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print(f'R2: {r2 : .4f}')

