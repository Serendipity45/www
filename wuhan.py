from pyecharts.charts import Line, Bar, Page
from pyecharts import options as opts
import pandas as pd

# 加载数据
data_path = 'data.csv'  # 请替换为您的数据文件路径
data = pd.read_csv(data_path)
data['date'] = pd.to_datetime(data['date'])

# 创建图表
line_chart = Line()
line_chart.add_xaxis(data['date'].dt.strftime('%Y-%m-%d').tolist())
line_chart.add_yaxis("客流量", data['flow'].tolist())

# 设置全局配置
line_chart.set_global_opts(title_opts=opts.TitleOpts(title="武汉地铁每日客流量趋势"),
                           xaxis_opts=opts.AxisOpts(type_="category", axislabel_opts=opts.LabelOpts(rotate=45)),
                           yaxis_opts=opts.AxisOpts(type_="value"))

# 设置系列配置
line_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))


data['weekday'] = data['date'].dt.weekday  # 0 是周一，6 是周日

# 计算每个工作日的平均客流量
weekday_flow = data.groupby('weekday')['flow'].mean().reset_index()

# 创建图表
bar_chart = Bar()
bar_chart.add_xaxis(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
bar_chart.add_yaxis("平均客流量", weekday_flow['flow'].tolist())

# 设置全局配置
bar_chart.set_global_opts(title_opts=opts.TitleOpts(title="周内平均客流量分析"),
                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                          yaxis_opts=opts.AxisOpts(type_="value"))

# 设置系列配置
bar_chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

data['month'] = data['date'].dt.month
month_flow = data.groupby('month')['flow'].mean().reset_index()

line_chart1 = Line()
line_chart1.add_xaxis(month_flow['month'].tolist())
line_chart1.add_yaxis("平均客流量", month_flow['flow'].tolist())

line_chart1.set_global_opts(title_opts=opts.TitleOpts(title="月度客流量变化"),
                           xaxis_opts=opts.AxisOpts(type_="category"),
                           yaxis_opts=opts.AxisOpts(type_="value"))

line_chart1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))


data['year'] = data['date'].dt.year

# 计算每年的平均客流量
year_flow = data.groupby('year')['flow'].mean().reset_index()

# 创建图表
line_chart2 = Line()
line_chart2.add_xaxis(year_flow['year'].astype(str).tolist())
line_chart2.add_yaxis("平均客流量", year_flow['flow'].tolist())

# 设置全局配置
line_chart2.set_global_opts(title_opts=opts.TitleOpts(title="年度客流量对比"),
                           xaxis_opts=opts.AxisOpts(type_="category"),
                           yaxis_opts=opts.AxisOpts(type_="value"))

# 设置系列配置
line_chart2.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

# 创建 Page 实例
page = Page()

# 假设 line_chart, bar_chart 等是您根据前面的示例代码创建的图表实例
# 这里我们仅以添加同一个 line_chart 为例进行演示，您应该替换为实际的图表变量

page.add(
    line_chart,  # 周内客流量分析图
    bar_chart,  # 月度客流量变化图
    line_chart1,
    line_chart2# 年度客流量对比图
    # 添加更多图表实例...
)

# 渲染页面到文件
page.render('wuhan_metro_flow_analysis.html')