import dearpygui.dearpygui as dpg
import csv
from ApproximatorModules.ModelBase import ModelsBase
import os
from joblib import dump, load
class NewModelWindow:
    controller: object
    xarr = []
    yarr = []
    def __init__(self, controller):
        self.controller = controller
    
    current_model_type = "Полиноминальный"
    
    def change_model_type(self, sender, app_data):
        self.current_model_type = app_data
        self.draw_hyperparams()

    def draw_hyperparams(self):
        """
        This function draws different input elements based on the current_model_type.
        It handles cases for "Полиноминальный", "Линейная регрессия", "Случайный лес", and "Дерево решений".
        """
        dpg.delete_item('hyperparams')
        with dpg.group(parent='hyperparams_group',tag='hyperparams'):
            match self.current_model_type:
                case "Полиноминальный":
                    with dpg.group(horizontal=True):
                        dpg.add_text("Степень:")
                        dpg.add_input_int(width=100, step=1, step_fast=1,default_value=5, tag="poly_num", min_value=1, min_clamped=True)
                case "Линейная регрессия":
                    with dpg.group(horizontal=True):
                        dpg.add_text("")
                case "Случайный лес":
                    with dpg.group(horizontal=False):
                        with dpg.group(horizontal=True):
                            dpg.add_text('max_depth')
                            dpg.add_input_int(width=100, step=1, step_fast=3, tag='max_depth',default_value=5, min_value=1, min_clamped=True)
                        with dpg.group(horizontal=True):
                            dpg.add_text('min_samples_split')
                            dpg.add_input_int(width=100, step=1, step_fast=3, tag='min_samples_split',default_value=2, min_value=1, min_clamped=True)
                        with dpg.group(horizontal=True):
                            dpg.add_text('min_samples_leaf')
                            dpg.add_input_int(width=100, step=1, step_fast=3, tag='min_samples_leaf',default_value=1, min_value=1, min_clamped=True)
                case "Дерево решений":
                    with dpg.group(horizontal=True):
                        dpg.add_text('Максимальная глубина')
                        dpg.add_input_int(width=100, step=1, step_fast=3, tag='max_depth',default_value=5, min_value=1, min_clamped=True)
    def ok_callback(self):
        model_type = ''
        hyperparams = {}
        match self.current_model_type:
            case "Полиноминальный":
                model_type = 'Poly'
                hyperparams = {'NumberPoly': dpg.get_value('poly_num')}
            case "Линейная регрессия":
                model_type = 'Linear'
                hyperparams = {}
            case "Случайный лес":
                model_type = 'RandomForest'
                hyperparams = {'max_depth': dpg.get_value('max_depth'),
                               'min_samples_split': dpg.get_value('min_samples_split'),
                               'min_samples_leaf': dpg.get_value('min_samples_leaf')}
            case "Дерево решений":
                model_type = 'Tree'
                hyperparams = {'max_depth': dpg.get_value('max_depth'),
                               'min_samples_split': dpg.get_value('min_samples_split'),
                               'min_samples_leaf': dpg.get_value('min_samples_leaf')}
        self.controller.add_tab(dpg.get_value('model_name'), model_type, hyperparams,self.xarr,self.yarr)
        dpg.delete_item('New Model')

    def cancel_callback(sender):
        dpg.delete_item('New Model')

    

    def file_select_callback(self, sender, app_data, user_data):
        for key in app_data["selections"]:
            file = open(app_data["selections"][key])
            file.name
            csv_data = list(csv.reader(file, delimiter=","))
            file.close()
            self.xarr = []
            self.yarr = []
            for i in csv_data:
                self.xarr.append(float(i[0]))
                self.yarr.append(float(i[1]))
            dpg.delete_item('selected file name')
            dpg.add_text('Выбран файл: ' + str(os.path.basename(app_data["selections"][key])),tag='selected file name', pos=[20, 270],parent='New Model')

    def openFile(self, sender, data):
        if not dpg.does_item_exist('file_dialog_id'):
            with dpg.file_dialog(directory_selector=False, show=False, callback=self.file_select_callback, file_count=1, id="file_dialog_id", width=800 ,height=400,min_size=[800, 400], max_size=[900, 600]):
                dpg.add_file_extension("*.csv{.csv}")
        dpg.show_item("file_dialog_id")
    def start(self):
        dpg.bind_font("Default font")
        with dpg.window(label="New Model", tag='New Model', no_resize=True, no_move=False, no_collapse=True, width=380, height=350, no_close=True):
            with dpg.group(horizontal=True, pos=[20, 40]):
                dpg.add_text("Имя:")
                dpg.add_input_text(width=285, tag='model_name',default_value='Lorem ipsum')
            with dpg.group(horizontal=True,pos=[20, 80]):
                dpg.add_text("Тип модели:")
                dpg.add_combo(items=["Полиноминальный", "Линейная регрессия", "Случайный лес", "Дерево решений"],default_value="Полиноминальный", width=215,callback=self.change_model_type)
                with dpg.group(tag="hyperparams_group", pos=[20, 120]):
                    dpg.add_group(tag="hyperparams")
                    self.draw_hyperparams()
            dpg.add_button(label="OK", width=50, height=25, pos=[225, 310], callback=self.ok_callback)
            dpg.add_button(label="Cancel", width=75, height=25, pos=[285, 310], callback=self.cancel_callback)
            
            dpg.add_text("Не выбрано файла",tag='selected file name', pos=[20, 270])
            dpg.add_button(label="Load file", width=150, height=25, pos=[20,310], callback=self.openFile)       


class MainGraphWindow:
    next_tab_id: int
    current_tab_id: int 
    controller: object
                
    def __init__(self):
        self.next_tab_id = 0
        self.current_tab_id = 0

    def show_file_dialog(self, sender, object):
        dpg.add_file_dialog()

    def tab_changed(self, sender, object):
        self.current_tab_id = object
        
    def add_model_tab(self, object):
        new_model_window = NewModelWindow(self.controller)
        new_model_window.start()
    def save_model_joblib(self, sender, object, current_model: ModelsBase):
        dump(current_model, "Model.joblib")

    def start(self, controller):
        self.controller = controller
        dpg.create_context()

        with dpg.font_registry():
            with dpg.font("fonts/notomono-regular.ttf", 20, default_font=True, tag="Default font") as f:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font("Default font")
        
        with dpg.window(tag="Primary Window"):
            with dpg.tab_bar(tag ="Tab_bar",callback=self.tab_changed):
                dpg.add_tab_button(label="+", callback=self.add_model_tab)

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 230, 230))
                dpg.add_theme_color(dpg.mvThemeCol_Tab, (230, 230, 230))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (180, 180, 180))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (180, 180, 180))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (180,180,180))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (255,255,255))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (230, 230, 230))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (230, 230, 230))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (230, 230, 230))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (200, 200, 200))


        dpg.bind_theme(container_theme)
        dpg.create_viewport(title='Le Module', width=1208, height=700, resizable=False)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        
    def print_callback(self, sender, data):
        print(data)
    def delete_tab(self):
        dpg.delete_item(self.current_tab_id)
    
    def change_line_color(self, sender, object, parent_name):
        object = [i * 255.0 for i in object]
        with dpg.theme_component(dpg.mvLineSeries, parent=parent_name):
                dpg.add_theme_color(dpg.mvPlotCol_Line, object, category=dpg.mvThemeCat_Plots)
    def change_scatter_color(self, sender, object, parent_name):
        object = [i * 255.0 for i in object]
        with dpg.theme_component(dpg.mvScatterSeries, parent=parent_name):
                dpg.add_theme_color(dpg.mvPlotCol_Line, object, category=dpg.mvThemeCat_Plots)

    def change_line_width(self, sender, object, parent_name):
        with dpg.theme_component(dpg.mvLineSeries, parent=parent_name):
                dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, float(object), category=dpg.mvThemeCat_Plots)
    def change_scatter_width(self, sender, object, parent_name):
        with dpg.theme_component(dpg.mvScatterSeries, parent=parent_name):
                dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, float(object), category=dpg.mvThemeCat_Plots)

    def add_tab(self, xarr, yarr, poly_xarr, poly_yarr, current_model: ModelsBase):
        self.next_tab_id += 1
        if (self.next_tab_id == 1):
            self.current_tab_id = dpg.add_tab(label=current_model.name, parent='Tab_bar', tag="Tab" + str(self.next_tab_id))
        else:
            dpg.add_tab(label=current_model.name, parent='Tab_bar', tag="Tab" + str(self.next_tab_id))

        with dpg.theme(tag="plot_theme" + str(self.next_tab_id)):
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (221, 132, 82), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 2, category=dpg.mvThemeCat_Plots)

            with dpg.theme_component(dpg.mvScatterSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (76, 114, 176), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Circle, category=dpg.mvThemeCat_Plots)
                dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 2, category=dpg.mvThemeCat_Plots)

        with dpg.group(parent="Tab" + str(self.next_tab_id)):
            with dpg.plot(tag="Graph" + str(self.next_tab_id), width=799, height=598, pos=(9, 39)):
                dpg.add_plot_axis(dpg.mvXAxis, label="X")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="y_axis" + str(self.next_tab_id))
                dpg.add_scatter_series(xarr, yarr, parent="y_axis" + str(self.next_tab_id), tag="scatter_data" + str(self.next_tab_id))
                dpg.add_line_series(poly_xarr, poly_yarr, parent="y_axis" + str(self.next_tab_id),tag="line_data" + str(self.next_tab_id))

            dpg.bind_item_theme("scatter_data" + str(self.next_tab_id), "plot_theme" + str(self.next_tab_id))
            dpg.bind_item_theme("line_data" + str(self.next_tab_id), "plot_theme" + str(self.next_tab_id))
            with dpg.group(horizontal=True, pos=[825,50], before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Название:")
                dpg.add_input_text(width=150, default_value=current_model.name, readonly=True)
                dpg.add_button(label="Сохранить", width=100, callback=self.save_model_joblib, user_data=current_model)
            with dpg.group(horizontal=True, pos=[825,85], before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Метод:")
                dpg.add_text(current_model.model_type)
                dpg.add_button(label="Удалить", pos=[1080,85], width=100, callback=self.delete_tab)
            with dpg.group(horizontal=False, pos=[825,120],before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Метрики:")
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика R^2:")
                    dpg.add_text(current_model.QualityMetrix['Метрика R^2'])
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика MSE:")
                    dpg.add_text(current_model.QualityMetrix['Метрика среднеквадратической ошибки'])   
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика средней ошибки:")
                    dpg.add_text(current_model.QualityMetrix['Метрика средней абсолютной ошибки'])   
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика максимальной ошибки:")
                    dpg.add_text(current_model.QualityMetrix['Метрика максимальной ошибки'])   
            with dpg.drawlist(width=1300, height=600, tag="drawlist" + str(self.next_tab_id)):
                dpg.draw_rectangle(pmin=[809.0, 2.0], pmax=[1198.0, 80.0], color=[0, 0, 0], thickness=1)
                dpg.draw_rectangle(pmin=[809.0, 80.0], pmax=[1198.0, 350.0], color=[0, 0, 0], thickness=1)
                dpg.draw_rectangle(pmin=[809.0, 350.0], pmax=[1198.0, 600.0], color=[0, 0, 0], thickness=1)

            with dpg.group(horizontal=True, pos=[825,400], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Толщина точек:")
                dpg.add_slider_float(default_value=2, width=200,callback=self.change_scatter_width, user_data="plot_theme" + str(self.next_tab_id),min_value=0.5, max_value=10,clamped=True)
            with dpg.group(horizontal=True, pos=[825,435], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Цвет точек:")
                dpg.add_color_edit(default_value=[76, 114, 176], no_inputs=True,callback=self.change_scatter_color, user_data="plot_theme" + str(self.next_tab_id))
            with dpg.group(horizontal=True, pos=[825,505], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Толщина линии:")
                dpg.add_slider_float(default_value=2, width=200,callback=self.change_line_width, user_data="plot_theme" + str(self.next_tab_id),min_value=0.5, max_value=10,clamped=True)
            with dpg.group(horizontal=True, pos=[825,540], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Цвет соединения:")
                dpg.add_color_edit(default_value=[221, 132, 82], no_inputs=True,callback=self.change_line_color, user_data="plot_theme" + str(self.next_tab_id))
