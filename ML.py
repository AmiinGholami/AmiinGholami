import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# خواندن داده‌ها از دیتابیس
conn = sqlite3.connect('cars.db')
df = pd.read_sql_query("SELECT * FROM cars", conn)
conn.close()

# پیش‌پردازش داده‌ها
df['kilometer'] = df['kilometer'].str.replace('کیلومتر', '').str.strip().astype(int)
df['year'] = df['year'].astype(int)
df['price'] = df['price'].astype(int)

# تبدیل شهر و مدل به داده‌های عددی
df = pd.get_dummies(df, columns=['city', 'model'])

# تعریف ویژگی‌ها و هدف
X = df.drop(columns=['id', 'price'])
y = df['price']

# تقسیم داده‌ها به مجموعه آموزش و تست
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ایجاد مدل و آموزش آن
model = LinearRegression()
model.fit(X_train, y_train)

# ارزیابی مدل
y_pred = model.predict(X_test)
print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))

# تابعی برای پیش‌بینی قیمت
def predict_price(model, kilometer, year, city, car_model):
    sample = pd.DataFrame([[kilometer, year] + [1 if city == col.split('_')[1] else 0 for col in X.columns if 'city_' in col] + [1 if car_model == col.split('_')[1] else 0 for col in X.columns if 'model_' in col]], columns=X.columns)
    return model.predict(sample)[0]

# نمونه پیش‌بینی
kilometer = 50000
year = 2018
city = 'تهران'
car_model = 'پژو 206'
predicted_price = predict_price(model, kilometer, year, city, car_model)
print('Predicted Price:', predicted_price)
