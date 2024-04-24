    from pyecharts.charts import Line, Page, Bar
    from pyecharts import options as opts
    import pandas as pd

    # 加载数据
    from pyecharts.components import Image
    from pyecharts.options import ComponentTitleOpts

    data_path = 'D:\WH_metro\data\data.csv'  # 请替换为您的数据文件路径
    data = pd.read_csv(data_path)
    data['date'] = pd.to_datetime(data['date'])

    # 创建图表
    line_chart = Line()
    line_chart.add_xaxis(data['date'].dt.strftime('%Y-%m-%d').tolist())
    line_chart.add_yaxis("客流量", data['flow'].tolist())

    # 设置全局配置
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title="客流量走势图"),
                            tooltip_opts=opts.TooltipOpts(trigger="axis"),
                            datazoom_opts=[
                                opts.DataZoomOpts(yaxis_index=0),
                                opts.DataZoomOpts(type_="inside", yaxis_index=0),
                            ],
                            visualmap_opts=opts.VisualMapOpts(
                                pos_top="10",
                                pos_right="10",
                                is_piecewise=True,
                                pieces=[
                                    {"gt": 0, "lte": 50, "color": "#096"},
                                    {"gt": 50, "lte": 100, "color": "#ffde33"},
                                    {"gt": 100, "lte": 150, "color": "#ff9933"},
                                    {"gt": 150, "lte": 200, "color": "#cc0033"},
                                    {"gt": 200, "lte": 300, "color": "#660099"},
                                    {"gt": 300, "color": "#7e0023"},
                                ],
                                out_of_range={"color": "#999"},
                            ),
                            xaxis_opts=opts.AxisOpts(type_="category"),
                            yaxis_opts=opts.AxisOpts(
                                type_="value",
                                name_location="start",
                                min_=0,
                                max_=500,
                                is_scale=True,
                                axistick_opts=opts.AxisTickOpts(is_inside=False),
                            ),
                            )

    # 设置系列配置
    line_chart.set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                {"yAxis": 50},
                {"yAxis": 100},
                {"yAxis": 150},
                {"yAxis": 200},
                {"yAxis": 300},
            ],
            label_opts=opts.LabelOpts(position="end"),
        ))
    line_chart.dump_options_with_quotes()
    # 渲染图表到文件
    line_chart.render('wuhan_metro_daily_flow_trend.html')


    # page_draggable_layout()
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

    csv_file_path = 'D:\WH_metro\data\daysort.csv'
    csv_data = pd.read_csv(csv_file_path)
    from collections import Counter
    all_ranks = pd.concat([csv_data['one'], csv_data['two'], csv_data['three'], csv_data['four'], csv_data['five']])
    station_frequencies = Counter(all_ranks)
    station_freq_df = pd.DataFrame(station_frequencies.items(), columns=['Station', 'Frequency']).sort_values(by='Frequency', ascending=False)

    # from pyecharts.charts import Bar, Line, Page
    from pyecharts.charts import Pie
    # from pyecharts import options as opts

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
        # radius=["30%", "75%"],  # 可以调整饼图的内半径和外半径来为标签留出空间
        center=["50%", "60%"],  # 调整饼图的中心位置
        # rosetype="radius",  # 如果您想要玫瑰图效果，可以使用"radius"或"area"
    )
    pie.set_global_opts(title_opts=opts.TitleOpts(title="武汉地铁站点客流量排名频次"),
                        legend_opts=opts.LegendOpts(pos_left="15%"),)
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

    dates = csv_data['date'].tolist()  # 日期列表
    rankings = []  # 存储每天的排名
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
            rankings.append(0)  # 如果当天没有排名，则标记为None
    # 使用Counter计算每个数字出现的次数
    print(rankings)
    counts = Counter(rankings)
    # 按照数字顺序对次数进行排序
    sorted_counts = sorted(counts.items(), key=lambda x: x[0])
    # 提取排序后的次数
    sorted_counts_values = [count for _, count in sorted_counts]
    # 输出结果
    print(sorted_counts_values)
    line = Line()
    line.add_xaxis(["无","1","2","3","4","5"])
    line.add_yaxis("排名", sorted_counts_values, is_connect_nones=True)
    line.set_global_opts(title_opts=opts.TitleOpts(title="2号线江汉路站时间序列分析"),
                        yaxis_opts=opts.AxisOpts(type_="value"),
                        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)))

    # image = Image()
    #
    # img_src = (
    #     "D:\WH_metro\data\武汉地铁线路图.jpg"
    # )
    # image.add(
    #     src=img_src,
    #     style_opts={"width": "200px", "height": "200px", "style": "margin-top: 20px"},
    # )
    # image.set_global_opts(
    #     title_opts=ComponentTitleOpts(title="武汉地铁路线图")
    # )


    # 创建 Page 实例
    page = Page(layout=Page.DraggablePageLayout)

    # 假设 line_chart, bar_chart 等是您根据前面的示例代码创建的图表实例
    # 这里我们仅以添加同一个 line_chart 为例进行演示，您应该替换为实际的图表变量

    page.add(
        line_chart,  # 周内客流量分析图
        bar_chart,  # 月度客流量变化图
        line_chart1,
        line_chart2,# 年度客流量对比图
        pie,
        line
        # 添加更多图表实例...
    )
    # page.add_js_funcs("D:\WH_metro\data\chart_config (1).json")

    # 渲染页面到文件
    page.render('wuhan_metro_flow_analysis.html')