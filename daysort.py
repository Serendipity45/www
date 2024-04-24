# Load the CSV file
import pandas as pd

csv_file_path = 'D:\WH_metro\data\daysort.csv'
csv_data = pd.read_csv(csv_file_path)

from collections import Counter

# Combine all rank columns for frequency analysis
all_ranks = pd.concat([csv_data['one'], csv_data['two'], csv_data['three'], csv_data['four'], csv_data['five']])

# Calculate the frequency of each station appearing in the top 5
station_frequencies = Counter(all_ranks)

# Convert the counter to a DataFrame for easier analysis and plotting
station_freq_df = pd.DataFrame(station_frequencies.items(), columns=['Station', 'Frequency']).sort_values(by='Frequency', ascending=False)

from pyecharts.charts import Bar, Line, Page
from pyecharts import options as opts

# Create a bar chart for station frequencies
from pyecharts.charts import Pie
from pyecharts import options as opts

# 假设 station_freq_df 包含站点和频次的数据
stations = station_freq_df['Station'].tolist()
frequencies = station_freq_df['Frequency'].tolist()

# 使用 station_freq_df 的数据
stations = station_freq_df['Station'].tolist()
frequencies = station_freq_df['Frequency'].tolist()

pie = Pie()
pie.add(
    series_name="",
    data_pair=[list(z) for z in zip(stations, frequencies)],
    radius=["30%", "75%"],  # 可以调整饼图的内半径和外半径来为标签留出空间
    center=["50%", "100%"],  # 调整饼图的中心位置
    rosetype="radius",  # 如果您想要玫瑰图效果，可以使用"radius"或"area"
)
pie.set_global_opts(title_opts=opts.TitleOpts(title="武汉地铁站点客流量排名频次"))

dates = csv_data['date'].tolist()  # 日期列表
rankings = []  # 存储每天的排名

# 遍历数据集，确定"2号线江汉路站"每天的排名
for index, row in csv_data.iterrows():
    if row['one'] == "2号线江汉路站":
        rankings.append(1)
    elif row['two'] == "2号线江汉路站":
        rankings.append(2)
    elif row['three'] == "2号线江汉路站":
        rankings.append(3)
    elif row['four'] == "2号线江汉路站":
        rankings.append(4)
    elif row['five'] == "2号线江汉路站":
        rankings.append(5)
    else:
        rankings.append(None)  # 如果当天没有排名，则标记为None

line = Line()
line.add_xaxis(dates)
line.add_yaxis("排名", rankings, is_connect_nones=True)
line.set_global_opts(title_opts=opts.TitleOpts(title="2号线江汉路站时间序列分析"),
                     yaxis_opts=opts.AxisOpts(type_="value", min_=1, max_=5),
                     xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)))

# 创建 Page 实例，整合多个图表
page = Page()
page.add(pie, line)

# 渲染页面到文件
page.render('jianghanlu_time_series1.html')
