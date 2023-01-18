import numpy as np
from bokeh.plotting import figure
from bokeh import models
from bokeh import layouts
from bokeh.models import Range1d

# The tools used in each bokeh figure.
TOOLS = "pan,wheel_zoom,box_zoom,reset"

# A mapping of country code to country name.
COUNTRYCODE2COUNTRY = {
    "at": "Austria",
    "be": "Belgium",
    "cz": "CzechRepublic",
    "dk": "Denmark",
    "fr": "France",
    "de": "Germany",
    "ie": "Ireland",
    "it": "Italy",
    "li": "Liechtenstein",
    "lu": "Luxembourg",
    "nl": "Netherlands",
    "pl": "Poland",
    "pt": "Portugal",
    "es": "Spain",
    "se": "Sweden",
    "ch": "Switzerland",
    "gb": "UK"
}


def candlesticks(data):
    regions = np.unique(data["region"])
    if len(regions) > 1:
        raise ValueError(f"The input data has multiple regions {regions}")
    region = COUNTRYCODE2COUNTRY[regions[0]]
    source = models.ColumnDataSource(data={
        "timestamp": data["timestamp"].astype("<i8") * 1000,  # Bokeh uses ms.
        "open": data["open"],
        "high": data["high"],
        "low": data["low"],
        "close": data["close"],
        "volume": data["volume"],
        "bottom": [0] * len(data),
        "width": [20 * 1000] * len(data),  # 20 sec width of candlesticks.
    })
    fig1 = figure(
        x_axis_type="datetime", width=1000, height=400,
        title=f"{region.title()} Candlestick", background_fill_color="#efefef",
        y_axis_label="Price [DKK]",
        tools=TOOLS,
    )
    fig1.toolbar.logo = None
    fig1.add_tools(models.HoverTool(
        tooltips=[
            ("timestamp", "@timestamp{%Y-%m-%d %H:%M:%S}"),
            ("open", "@open"),
            ("high", "@high"),
            ("low", "@low"),
            ("close", "@close"),
            ("volume", "@volume"),
        ],
        formatters={"@timestamp": "datetime"}
    ))
    fig1.xaxis.axis_label_text_font_style = "normal"
    fig1.yaxis.axis_label_text_font_style = "normal"
    fig1.y_range = Range1d(
        min(
            min(source.data["open"]),
            min(source.data["high"]),
            min(source.data["low"]),
            min(source.data["close"]),
        ),
        1.1 * max(
            max(source.data["open"]),
            max(source.data["high"]),
            max(source.data["low"]),
            max(source.data["close"]),
        )
    )
    fig1.xaxis.major_label_orientation = np.pi / 4  # radians
    fig1.segment(
        "timestamp", "high", "timestamp", "low", color="black", source=source
    )
    fig1.vbar(
        "timestamp", "width", "open", "close",
        color="#eb3c40", line_width=2,
        source=source,
        view=models.CDSView(filter=models.BooleanFilter(list(data["close"] <= data["open"])))
    )
    fig1.vbar(
        "timestamp", "width", "open", "close", fill_color="white",
        line_color="#49a3a3", line_width=2,
        source=source,
        view=models.CDSView(filter=models.BooleanFilter(list(data["close"] > data["open"])))
    )
    fig2 = figure(
        x_axis_type="datetime", width=1000, height=200,
        background_fill_color="#efefef",
        x_axis_label="Timestamp",
        y_axis_label="Volume [MWh]",
        tools=TOOLS,
    )
    fig2.toolbar.logo = None
    fig2.add_tools(models.HoverTool(
        tooltips=[
            ("timestamp", "@timestamp{%Y-%m-%d %H:%M:%S}"),
            ("open", "@open"),
            ("high", "@high"),
            ("low", "@low"),
            ("close", "@close"),
            ("volume", "@volume"),
        ],
        formatters={"@timestamp": "datetime"}
    ))
    fig2.x_range = fig1.x_range
    fig2.xaxis.axis_label_text_font_style = "normal"
    fig2.yaxis.axis_label_text_font_style = "normal"
    fig2.vbar(
        x="timestamp", width="width", bottom="bottom", top="volume",
        source=source, alpha=0.5
    )
    fig = layouts.column(children=[fig1, fig2])
    return fig
