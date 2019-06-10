import datetime


day1 = datetime.date.today()    # 今日を取得(時間は含まず)
day2 = day1 + datetime.timedelta(days=1)  # 1日加算

print(day1.strftime("%Y-%m-%d"))  # datetimeのフォーマット
print(day2.strftime("%Y-%m-%d"))  # datetimeのフォーマット
