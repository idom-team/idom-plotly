import { default as PlotlyPlot } from "react-plotly.js";

import React from "react";
import ReactDOM from "react-dom";
import htm from "htm";

const html = htm.bind(React.createElement);

export function bind(node, config) {
  return {
    create: (component, props, children) =>
      React.createElement(component, props, ...children),
    render: (element) => ReactDOM.render(element, node),
    unmount: () => ReactDOM.unmountComponentAtNode(node),
  };
}

export function Plot({ onRelayout, ...props }) {
  const figure = React.useRef(null);

  let onUpdate, onInitialized;
  onUpdate = onInitialized = (newFigure) => {
    figure.current = newFigure;
  };

  return React.createElement(PlotlyPlot, {
    ...wrapEventHandlers(props),
    onUpdate,
    onInitialized,
    onRelayout: makeJsonSafeEventHandler(
      makeHandlerWithFigureData(onRelayout, figure)
    ),
  });
}

function wrapEventHandlers(props) {
  const newProps = Object.assign({}, props);
  for (const [key, value] of Object.entries(props)) {
    if (typeof value === "function") {
      newProps[key] = makeJsonSafeEventHandler(value);
    }
  }
  return newProps;
}

function makeJsonSafeEventHandler(oldHandler, figure) {
  return function safeEventHandler(data) {
    if (!data) {
      oldHandler(null, null);
      return;
    }

    const event = data.event;
    delete data.event;

    oldHandler(event, serializePlotlyEvent(data));
  };
}

function makeHandlerWithFigureData(oldHandler, figureRef) {
  return function eventHandler(data) {
    oldHandler(event, {
      ...data,
      figure: serializePlotlyFigure(figureRef.current),
    });
  };
}

function serializePlotlyFigure(figure) {
  if (!figure) {
    return null;
  }
  return { layout: figure.layout };
}

// issue: https://github.com/plotly/plotly.py/issues/3550
// copied from: https://github.com/plotly/plotly.py/blob/cfad7862594b35965c0e000813bd7805e8494a5b/packages/javascript/jupyterlab-plotly/src/Figure.ts#L1295-L1300

function serializePlotlyEvent(data) {
  return {
    points: buildPointsObject(data),
    device_state: buildInputDeviceStateObject(data),
    selector: buildSelectorObject(data),
  };
}

function buildPointsObject(data) {
  var pointsObject;
  if (data.hasOwnProperty("points")) {
    // Most cartesian plots
    var pointObjects = data["points"];
    var numPoints = pointObjects.length;

    var hasNestedPointObjects = true;
    for (let i = 0; i < numPoints; i++) {
      hasNestedPointObjects =
        hasNestedPointObjects && pointObjects[i].hasOwnProperty("pointNumbers");
      if (!hasNestedPointObjects) break;
    }
    var numPointNumbers = numPoints;
    if (hasNestedPointObjects) {
      numPointNumbers = 0;
      for (let i = 0; i < numPoints; i++) {
        numPointNumbers += pointObjects[i]["pointNumbers"].length;
      }
    }
    pointsObject = {
      trace_indexes: new Array(numPointNumbers),
      point_indexes: new Array(numPointNumbers),
      xs: new Array(numPointNumbers),
      ys: new Array(numPointNumbers),
    };

    if (hasNestedPointObjects) {
      var flatPointIndex = 0;
      for (var p = 0; p < numPoints; p++) {
        for (
          let i = 0;
          i < pointObjects[p]["pointNumbers"].length;
          i++, flatPointIndex++
        ) {
          pointsObject["point_indexes"][flatPointIndex] =
            pointObjects[p]["pointNumbers"][i];
          // also add xs, ys and traces so that the array doesn't get truncated later
          pointsObject["xs"][flatPointIndex] = pointObjects[p]["x"];
          pointsObject["ys"][flatPointIndex] = pointObjects[p]["y"];
          pointsObject["trace_indexes"][flatPointIndex] =
            pointObjects[p]["curveNumber"];
        }
      }

      let single_trace = true;
      for (let i = 1; i < numPointNumbers; i++) {
        single_trace =
          single_trace &&
          pointsObject["trace_indexes"][i - 1] ===
            pointsObject["trace_indexes"][i];
        if (!single_trace) break;
      }
      if (single_trace) {
        pointsObject["point_indexes"].sort(function (a, b) {
          return a - b;
        });
      }
    } else {
      for (var p = 0; p < numPoints; p++) {
        pointsObject["trace_indexes"][p] = pointObjects[p]["curveNumber"];
        pointsObject["point_indexes"][p] = pointObjects[p]["pointNumber"];
        pointsObject["xs"][p] = pointObjects[p]["x"];
        pointsObject["ys"][p] = pointObjects[p]["y"];
      }
    }

    // Add z if present
    var hasZ =
      pointObjects[0] !== undefined && pointObjects[0].hasOwnProperty("z");
    if (hasZ) {
      pointsObject["zs"] = new Array(numPoints);
      for (p = 0; p < numPoints; p++) {
        pointsObject["zs"][p] = pointObjects[p]["z"];
      }
    }

    return pointsObject;
  } else {
    return null;
  }
}

/**
 * Build InputDeviceState data structure from data supplied by the
 * plotly_click, plotly_hover, or plotly_select events
 * @param {Object} data
 * @returns {null|InputDeviceState}
 */
function buildInputDeviceStateObject(data) {
  var event = data["event"];
  if (event === undefined) {
    return null;
  } else {
    var inputDeviceState = {
      // Keyboard modifiers
      alt: event["altKey"],
      ctrl: event["ctrlKey"],
      meta: event["metaKey"],
      shift: event["shiftKey"],

      // Mouse buttons
      button: event["button"],
      buttons: event["buttons"],
    };
    return inputDeviceState;
  }
}

/**
 * Build Selector data structure from data supplied by the
 * plotly_select event
 * @param data
 * @returns {null|Selector}
 */
function buildSelectorObject(data) {
  var selectorObject;

  if (data.hasOwnProperty("range")) {
    // Box selection
    selectorObject = {
      type: "box",
      selector_state: {
        xrange: data["range"]["x"],
        yrange: data["range"]["y"],
      },
    };
  } else if (data.hasOwnProperty("lassoPoints")) {
    // Lasso selection
    selectorObject = {
      type: "lasso",
      selector_state: {
        xs: data["lassoPoints"]["x"],
        ys: data["lassoPoints"]["y"],
      },
    };
  } else {
    selectorObject = null;
  }
  return selectorObject;
}
