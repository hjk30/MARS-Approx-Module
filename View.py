import dearpygui.dearpygui as dpg
import csv
from ApproximatorModules.ModelBase import ModelsBase

class NewModelWindow:
    controller: object

    def __init__(self, controller):
        self.controller = controller

    def file_select_callback(sender, app_data, user_data):
        for key in app_data["selections"]:
            file = open(app_data["selections"][key])
            csv_data = list(csv.reader(file, delimiter=","))
            file.close()
            global xarr
            global yarr
            xarr = []
            yarr = []
            j = 0.0
            for i in csv_data:
                j+=1.0
                xarr.append(j)
                yarr.append(float(i[0]))
    
    current_model_type = "Полиноминальный"
    
    def change_model_type(self, sender, app_data):
        self.current_model_type = app_data
        self.draw_hyperparams()

    def draw_hyperparams(self):
        dpg.delete_item('hyperparams')
        with dpg.group(parent='hyperparams_group',tag='hyperparams'):
            match self.current_model_type:
                case "Полиноминальный":
                    with dpg.group(horizontal=True,pos=[150, 90]):
                        dpg.add_text("Степень:")
                        dpg.add_input_int(width=100, step=0, step_fast=0,default_value=5, tag="poly_num", min_value=1)
                case "Линейная регрессия":
                    with dpg.group(horizontal=True, pos=[150, 90]):
                        dpg.add_text("")
                case "Случайный лес":
                    with dpg.group(horizontal=True, pos=[150, 90]):
                        dpg.add_text('Максимальная глубина')
                        dpg.add_input_int(width=100, step=1, step_fast=3, tag='max_depth',default_value=5, min_value=1)
                case "Дерево решений":
                    with dpg.group(horizontal=True, pos=[150, 90]):
                        dpg.add_text('Максимальная глубина')
                        dpg.add_input_int(width=100, step=1, step_fast=3, tag='max_depth',default_value=5, min_value=1)
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
                model_type = 'Tree'
                hyperparams = {'max_depth': dpg.get_value('max_depth')}
            case "Дерево решений":
                model_type = 'RandomForest'
                hyperparams = {'max_depth': dpg.get_value('max_depth')}
        self.controller.add_tab(dpg.get_value('model_name'), model_type, hyperparams)
        dpg.delete_item('New Model')

    def cancel_callback(sender):
        dpg.delete_item('New Model')
    """
    with dpg.file_dialog(directory_selector=True,show=False,tag="file_load_id", file_count=1, width=800 ,height=400):
        dpg.add_file_extension(".*")
         dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension("Source files (*.csv){.csv}", color=(0, 255, 255, 255))
    file_data = []
    file_data = 
    """
    def start(self):
        dpg.bind_font("Default font")
        with dpg.window(label="New Model", tag='New Model', no_resize=True, no_move=False, no_collapse=True, width=500, height=400, no_close=True):
            with dpg.group(horizontal=True, pos=[150, 25]):
                dpg.add_text("Имя:")
                dpg.add_input_text(width=170, tag='model_name',default_value='Lorem ipsum')
            with dpg.group(horizontal=True,pos=[150, 60]):
                dpg.add_text("Тип модели:")
                dpg.add_combo(items=["Полиноминальный", "Линейная регрессия", "Случайный лес", "Дерево решений"],default_value="Полиноминальный", width=200,callback=self.change_model_type)
                with dpg.group(tag="hyperparams_group"):
                    dpg.add_group(tag="hyperparams")
                    self.draw_hyperparams()
            dpg.add_button(label="OK", width=50, height=25, pos=[300, 290], callback=self.ok_callback)
            dpg.add_button(label="Cancel", width=75, height=25, pos=[360, 290], callback=self.cancel_callback)
            #dpg.add_button(label="Load file", width=150, height=50, pos=[20,290], dpg.show_item("file_load_id"))       


class MainGraphWindow:
    next_tab_id: int
    current_tab_id: int 
    controller: object
                
    def __init__(self):
        self.next_tab_id = 0
        self.current_tab_id = 0
        print("init")

    def show_file_dialog(self, sender, object):
        dpg.add_file_dialog()

    def tab_changed(self, sender, object):
        self.current_tab_id = object
        
    def add_model_tab(self, object):
        new_model_window = NewModelWindow(self.controller)
        new_model_window.start()
        #self.controller.add_tab('Model' + str(self.next_tab_id), 'Poly', {'NumberPoly': 5})

    def start(self, controller):
        self.controller = controller
        dpg.create_context()

        with dpg.font_registry():
            with dpg.font("fonts/notomono-regular.ttf", 20, default_font=True, tag="Default font") as f:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

        dpg.bind_font("Default font")

        with dpg.file_dialog(directory_selector=False, show=False, file_count=1, id="file_dialog_id", width=800 ,height=400):
            dpg.add_file_extension(".*")
            dpg.add_file_extension("", color=(150, 255, 150, 255))
            dpg.add_file_extension("Source files (*.csv){.csv}", color=(0, 255, 255, 255))
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

    def add_tab(self, xarr, yarr, poly_xarr, poly_yarr, current_model: ModelsBase):
        self.next_tab_id += 1
        if (self.next_tab_id == 1):
            self.current_tab_id = dpg.add_tab(label=current_model.name, parent='Tab_bar', tag="Tab" + str(self.next_tab_id))
        else:
            dpg.add_tab(label=current_model.name, parent='Tab_bar', tag="Tab" + str(self.next_tab_id))
        #dpg.delete_item("Tab" + str(len(self.models) - 1))
        with dpg.group(parent="Tab" + str(self.next_tab_id)):
            with dpg.plot(tag="Graph" + str(self.next_tab_id), width=799, height=598, pos=(9, 39)):
                dpg.add_plot_axis(dpg.mvXAxis, label="X")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="y_axis" + str(self.next_tab_id))
                dpg.add_scatter_series(xarr, yarr, parent="y_axis" + str(self.next_tab_id))
                dpg.add_line_series(poly_xarr, poly_yarr, parent="y_axis" + str(self.next_tab_id))
            with dpg.group(horizontal=True, pos=[825,50], before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Название:")
                dpg.add_input_text(width=150, default_value=current_model.name)
                dpg.add_button(label="Сохранить", width=100)
            with dpg.group(horizontal=True, pos=[825,85], before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Метод:")
                dpg.add_text(current_model.model_type)
                dpg.add_button(label="Удалить модель", width=150, callback=self.delete_tab)
                #dpg.add_button(label="Выбрать данные", width=120, callback=self.show_file_dialog)
            with dpg.group(horizontal=False, pos=[825,120],before= "drawlist" + str(self.next_tab_id)):
                dpg.add_text("Метрики:")
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика R^2:")
                    dpg.add_text(current_model.QualityMetrix['Метрика R^2'])
                with dpg.group(horizontal=True,before= "drawlist" + str(self.next_tab_id)):
                    dpg.add_text("Метрика MSE:")
                    dpg.add_text(current_model.QualityMetrix['Метрика среднеквадратической ошибки'])   
            with dpg.drawlist(width=1300, height=600, tag="drawlist" + str(self.next_tab_id)):
                dpg.draw_rectangle(pmin=[809.0, 2.0], pmax=[1198.0, 80.0], color=[0, 0, 0], thickness=1)
                dpg.draw_rectangle(pmin=[809.0, 80.0], pmax=[1198.0, 350.0], color=[0, 0, 0], thickness=1)
                dpg.draw_rectangle(pmin=[809.0, 350.0], pmax=[1198.0, 600.0], color=[0, 0, 0], thickness=1)

            with dpg.group(horizontal=True, pos=[825,440], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Толщина точек:")
                dpg.add_combo(items=["0,5 pt", "1 pt", "2 pt", "4 pt", "6 pt"], default_value="1 pt", width=80)
            with dpg.group(horizontal=True, pos=[825,475], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Цвет точек:")
                dpg.add_color_edit(default_value=[0, 0, 0], no_inputs=True)
            with dpg.group(horizontal=True, pos=[825,530], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Вид линии:")
                dpg.add_combo(items=["Непрервыная", "Пунктирная"], width=150, default_value="Непрервыная")
            with dpg.group(horizontal=True, pos=[825,565], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Толщина линии:")
                dpg.add_combo(items=["0.5 pt", "1 pt", "2 pt", "4 pt", "6 pt"], default_value="1 pt", width=80)
            with dpg.group(horizontal=True, pos=[825,600], before="drawlist" + str(self.next_tab_id)):
                dpg.add_text("Цвет соединения:")
                dpg.add_color_edit(default_value=[0, 0, 0], no_inputs=True)