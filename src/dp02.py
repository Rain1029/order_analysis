import requests
import pypinyin
import csv
from functools import lru_cache

@lru_cache(maxsize=None)
def fetch_weather(cityname):
    url = f"https://wttr.in/{cityname}?format=j1"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()   
        data = resp.json()
        currentweather = data["current_condition"][0]
        return currentweather["temp_C"]
    except :
        print('访问出错')

def fill_weather_to_csv():
    # 打开raw_orders.csv，读取所有的内容，按行循环读取
    with open('data/raw_orders.csv',"r", encoding='utf-8') as f:
        reader = csv.DictReader(f)        # 自动用第一行作为 keys
        data = list(reader)
    for d in data:
        if d["city"].strip != "":
            cityname = "".join(pypinyin.lazy_pinyin(d["city"]))#根据城市中文名字，获取拼音的名字
            # print(cityname)
            temp = fetch_weather(cityname) #根据城市拼音名字获取气温
            d["temp"] = temp
        else:
            d["temp"] = "未知"

    with open('data/weather_orders.csv',"w",newline = '', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[1].keys()))
        writer.writeheader()
        writer.writerows(data)


if __name__=="__main__":
    print(fetch_weather("linyi"))
    fill_weather_to_csv()
