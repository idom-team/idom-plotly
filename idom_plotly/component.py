from __future__ import annotations

from pathlib import Path
from typing import Awaitable, Callable, Any, TypedDict, Union

from idom import VdomDict
from idom.web.module import export, module_from_file


_js_module = module_from_file(
    "idom-plotly-react",
    file=Path(__file__).parent / "bundle.js",
    fallback="⏳",
)
_Plot = export(_js_module, "Plot")


def Plot(props: Union[PropsDict, None] = None) -> VdomDict:
    return _Plot(props or {})


PlotlyEventHandler = Callable[[Any, Any], Union[None, Awaitable[None]]]


class PropsDict(TypedDict):
    # Basic Props
    data: Any
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

    # Event Hanler Props
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
