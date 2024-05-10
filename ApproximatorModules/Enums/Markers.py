from enum import Enum
import dearpygui.dearpygui as dpg

class Markers(Enum):
    CIRCLE = dpg.mvPlotMarker_Circle
    SQUARE = dpg.mvPlotMarker_Square
    DIAMOND = dpg.mvPlotMarker_Diamond
    CROSS = dpg.mvPlotMarker_Cross
    DOWN = dpg.mvPlotMarker_Down
    LEFT = dpg.mvPlotMarker_Left
    RIGHT = dpg.mvPlotMarker_Right
    PLUS = dpg.mvPlotMarker_Plus
    UP = dpg.mvPlotMarker_Up
    ASTERISK = dpg.mvPlotMarker_Asterisk