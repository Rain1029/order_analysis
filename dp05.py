import pandas as pd

def train_model(daily,isDrawFigure):
    from sklearn.model_selection import train_test_split
    X = daily[['avg_amount', 'total_amount']]   # 特征（2 列，注意双括号！）
    y = daily['sales']                  # 标签（1 列，Series 不是 DataFrame）

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,           # 20% 作测试
        random_state=42,         # 固定随机种子（保证全班结果一致）
    )
    print(f'训练集: {X_train.shape}, 测试集: {X_test.shape}')
    # 训练集: (292, 2), 测试集: (73, 2)
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_train, y_train)    
    # 在测试集上预测
    y_pred = model.predict(X_test)

    # 对比真实 vs 预测
    result = pd.DataFrame({
        '真实': y_test.values,
        '预测': y_pred,
        '误差': y_test.values - y_pred,
    })
    print(result.head(10))
    from sklearn.metrics import mean_squared_error,r2_score
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    ## print(f"{r2=}{mse=}")
    if isDrawFigure:
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['SimHei']   # 中文
        plt.rcParams['axes.unicode_minus'] = False

        residuals = y_test - y_pred

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # 左图：残差 vs 预测值
        axes[0].scatter(y_pred, residuals, alpha=0.5)
        axes[0].axhline(0, color='red', linestyle='--')
        axes[0].set_xlabel('预测值')
        axes[0].set_ylabel('残差')
        axes[0].set_title('残差 vs 预测值')

        # 右图：残差直方图
        axes[1].hist(residuals, bins=20, edgecolor='black')
        axes[1].axvline(0, color='red', linestyle='--')
        axes[1].set_xlabel('残差')
        axes[1].set_ylabel('频数')
        axes[1].set_title('残差分布')

        plt.tight_layout()
        plt.show()
        fig.savefig('pic/001.png', dpi=150, bbox_inches='tight')
        # 假设已有 y_test 和 y_pred
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.scatter(y_test, y_pred, alpha=0.5, s=30)

        # 画对角线（理想情况：y = x）
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2)

        ax.set_xlabel('真实值（订单数）')
        ax.set_ylabel('预测值（订单数）')
        ax.set_title(f'真实 vs 预测（R² = {r2:.3f}）')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        fig.savefig('pic/002.png', dpi=150, bbox_inches='tight')
        plt.show()

        features = ['avg_amount', 'total_amount']
        coefs = model.coef_
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.barh(features, coefs, color='steelblue')
        ax.set_xlabel('系数（影响大小）')
        ax.set_title('特征重要性')
        ax.axvline(0, color='black', linewidth=0.5)
        plt.tight_layout()
        fig.savefig('pic/003.png', dpi=150, bbox_inches='tight')
        plt.show()
    return model,mse,r2

def read_data(filename):
    df = pd.read_csv(filename)
    df['order_date'] = pd.to_datetime(df['order_date'])
    # 2. 丢弃 amount 为空
    df = df.dropna(subset=['amount'])
    # 3. 去重
    df = df.drop_duplicates(subset=['order_id'])
    # 4. 填充 category
    df['category'] = df['category'].fillna('未知')

    # 按日期聚合
    daily = df.groupby(df['order_date'].dt.date).agg(
        sales=('order_id', 'count'),         # 当天订单数（标签 y）
        avg_amount=('amount', 'mean'),       # 当天平均金额（特征 1）
        temp=('temp', 'mean'),               # 当天平均温度（特征 2）
        total_amount=('amount', 'sum'),       # 当天平均金额（特征 3）
    ).reset_index()
    return daily
##########################33333333333333333
if os.path.exists("model/mymodel.mdl"):
    with open("model/mymodel.mdl", "rb") as f:
        model = pickle.load(f)
else:
    d = read_data("data/weather_orders2.csv")
    model, mse, r2 = train_model(d, True)
    with open("model/mymodel.mdl", "wb") as f:



#d = read_data("data/weather_orders.csv")
model,mse,r2 = train_model(d, True)
print(f"{mse=}{r2=}")
tomorrow = pd.DataFrame({'avg_amount': [1000], 'total_amount': [10000]})
predicted_sales = model.predict(tomorrow)
print(f'预测明天订单数: {predicted_sales[0]:.0f}')







