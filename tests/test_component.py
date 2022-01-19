import idom
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from idom_plotly.component import Plot
import plotly.express as px


def test_plot_from_dict(driver: WebDriver, driver_wait_until, display):
    event_args = idom.Ref(None)

    display(
        lambda: Plot(
            {
                "data": [
                    {
                        "x": [1, 2, 3],
                        "y": [2, 6, 3],
                        "type": "scatter",
                        "mode": "lines+markers",
                        "marker": {"color": "red"},
                    },
                    {
                        "type": "bar",
                        "x": [1, 2, 3],
                        "y": [2, 5, 3],
                    },
                ],
                "onClick": lambda *args: event_args.set_current(args),
            }
        )
    )

    plotly = driver.find_element("class name", "plotly")

    ActionChains(driver).move_to_element_with_offset(plotly, 342, 107).click().perform()

    driver_wait_until(lambda: event_args.current is not None)

    assert event_args.current == (
        {
            "isTrusted": True,
            "pointerX": 342,
            "pointerY": 107,
        },
        {
            "device_state": None,
            "points": {
                "point_indexes": [1],
                "trace_indexes": [0],
                "xs": [2],
                "ys": [6],
            },
            "selector": None,
        },
    )


def test_plot_from_figure(driver: WebDriver, driver_wait_until, display):
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x="year", y="pop")

    event_args = idom.Ref(None)

    display(
        lambda: Plot(
            fig,
            {
                "onClick": lambda *args: event_args.set_current(args),
            },
        )
    )

    plotly = driver.find_element("class name", "plotly")

    ActionChains(driver).move_to_element_with_offset(plotly, 335, 184).click().perform()

    driver_wait_until(lambda: event_args.current is not None)

    assert event_args.current == (
        {
            "isTrusted": True,
            "pointerX": 335,
            "pointerY": 184,
        },
        {
            "points": {
                "trace_indexes": [0],
                "point_indexes": [5],
                "xs": [1977],
                "ys": [23796400],
            },
            "device_state": None,
            "selector": None,
        },
    )
