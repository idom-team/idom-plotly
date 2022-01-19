from __future__ import annotations

import json
from pathlib import Path
from typing import Awaitable, Callable, Any, TypedDict, Union, cast

from idom import VdomDict
from idom.web.module import export, module_from_file
from plotly.basedatatypes import BaseFigure


_js_module = module_from_file(
    "idom-plotly-react",
    file=Path(__file__).parent / "bundle.js",
    fallback="⏳",
)
_Plot = export(_js_module, "Plot")


def Plot(
    figure: BaseFigure | FigureDict | PropsDict,
    event_handlers: PropsDict | None = {},
) -> VdomDict:
    """Return an IDOM component for displaying Plotly figures

    Parameters:
        figure:
            The plotly figure. May be specified using a Figure object or a JSON
            serializable dictionary which contains plotly figure data.
        event_handlers:
            The event handlers which should be bound to the figure. These handlers may
            be functions or coroutines of the form ``(event, data) -> None``. Each
            handler is bound to an event type base on its key in the given dictionary.
            For example a handler bound to the key ``onClick`` will respond to and
            recieve data related to click events initiated by a user.
    """
    props: PropsDict = {}

    if isinstance(figure, BaseFigure):
        # plotly does not have a public method for making a json dict
        figure = cast(FigureDict, json.loads(figure.to_json()))

    props.update(figure)  # type: ignore

    if event_handlers:
        props.update(event_handlers)

    return _Plot(props)


PlotlyEventHandler = Callable[[Any, Any], Union[Awaitable[None], None]]


class FigureDict(TypedDict, total=False):
    """Standard Plotly fields"""

    data: list[dict[str, Any]]
    layout: Any
    frames: Any
    config: Any
    revision: Any
    onInitialized: Any
    onUpdate: Any
    onPurge: Any
    onError: Any
    divId: Any
    className: Any
    style: Any
    debug: Any
    useResizeHandler: Any


class EventHandlersDict(TypedDict, total=False):
    """Event handlers defined by react-plotly"""

    onAfterExport: PlotlyEventHandler
    onAfterPlot: PlotlyEventHandler
    onAnimated: PlotlyEventHandler
    onAnimatingFrame: PlotlyEventHandler
    onAnimationInterrupted: PlotlyEventHandler
    onAutoSize: PlotlyEventHandler
    onBeforeExport: PlotlyEventHandler
    onBeforeHover: PlotlyEventHandler
    onButtonClicked: PlotlyEventHandler
    onClick: PlotlyEventHandler
    onClickAnnotation: PlotlyEventHandler
    onDeselect: PlotlyEventHandler
    onDoubleClick: PlotlyEventHandler
    onFramework: PlotlyEventHandler
    onHover: PlotlyEventHandler
    onLegendClick: PlotlyEventHandler
    onLegendDoubleClick: PlotlyEventHandler
    onRelayout: PlotlyEventHandler
    onRelayouting: PlotlyEventHandler
    onRestyle: PlotlyEventHandler
    onRedraw: PlotlyEventHandler
    onSelected: PlotlyEventHandler
    onSelecting: PlotlyEventHandler
    onSliderChange: PlotlyEventHandler
    onSliderEnd: PlotlyEventHandler
    onSliderStart: PlotlyEventHandler
    onSunburstClick: PlotlyEventHandler
    onTransitioning: PlotlyEventHandler
    onTransitionInterrupted: PlotlyEventHandler
    onUnhover: PlotlyEventHandler
    onWebGlContextLost: PlotlyEventHandler


class PropsDict(FigureDict, EventHandlersDict):
    """All valid fields"""
