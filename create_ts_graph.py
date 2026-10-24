from datetime import datetime

def convert_timeseries(timeseries_list):
    return [
        datetime.fromisoformat(ts.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        for ts in timeseries_list
    ]

def create_graph(timeseries_list):
    import numpy as np
    import polars as pl
    from flexviz import Dashboard
    n = len(timeseries_list)
    value = np.array([i for i in range(len(timeseries_list))])
    timeseries_list = convert_timeseries(timeseries_list)
    timeseries_list = sorted(timeseries_list)
    df = pl.DataFrame({
        "timestamp":timeseries_list
    })
    df = df.with_columns(
        pl.col("timestamp")
        .str.to_datetime(time_zone="UTC")
        .dt.date()
    )
    timeseries_list = df["timestamp"].to_numpy()
    df = pl.select(timestamp=timeseries_list,value=pl.Series(value))
    
    dash = Dashboard(df,cache=True)
    # 1. Line chart
    dash.add_figure(title="Line Chart") \
        .add_line(x="timestamp", y="value", n_points=2000)

    # 2. Histogram
    dash.add_figure(title="Histogram") \
        .add_histogram(x="value", bins=50)

    # 3. Box plot
    dash.add_figure(title="Box Plot") \
        .add_boxplot(y="value")

    # 4. Bar chart
    dash.add_figure(title="Bar Chart") \
        .add_bar(labels="timestamp", values="value", agg="mean")

    # 5. Pie chart
    dash.add_figure(title="Pie Chart") \
        .add_pie(labels="timestamp", values="value", agg="mean")

    # 6. Treemap — corrected
    dash.add_figure(title="Treemap") \
        .add_treemap(path=["timestamp"], values="value", agg="mean")

    # 7. 2D histogram
    dash.add_figure(title="2D Histogram") \
        .add_histogram2d(x="timestamp", y="value", x_bins=30, y_bins=30)

  
    return dash

def show_ts_webapp(dash):
    import numpy as np
    import polars as pl
    from flexviz import Dashboard
    dash.show()
    

if __name__=="__main__":
    N = pow(10,6)
    timeseries_list = [
    "2026-10-24T10:00:00Z",
    ]*(N)
    dash = create_graph(timeseries_list)
    show_ts_webapp(dash)
