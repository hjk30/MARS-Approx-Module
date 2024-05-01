import dearpygui.dearpygui as dpg
import csv
import numpy as np
import random as rnd

def SetTooltip(text):
    with dpg.tooltip(dpg.last_item()): dpg.add_text(text)

xarr = []
yarr = []
poly_xarr = []
poly_yarr = []
for i in range(0,25):
    xarr.append(i)
    yarr.append(i*i + 2 * i + 10 + np.random.uniform(-50,50))
 
def BtnDrawGraph():
    with dpg.stage(tag="Stage1"):
        with dpg.plot(tag="Graph", width=399, height=599, pos=(9, 98)):
            dpg.add_plot_axis(dpg.mvXAxis, label="X")
            dpg.add_plot_axis(dpg.mvYAxis, label="Y", tag="y_axis")
            dpg.add_scatter_series(xarr, yarr, parent="y_axis")
            if (len(poly_yarr) != 0):
                dpg.add_line_series(poly_xarr, poly_yarr, parent="y_axis")

    dpg.move_item(item="Graph", parent="Primary Window")

def PolyAprox(x,y):

    coeff = np.polyfit(x, y, dpg.get_value("poly_num"))
    predict = np.poly1d(coeff)
    ret = []
    i = 0
    while(i < len(x)):
        ret.append(predict(x[i]))
        i+=1
    return ret

def BtnAprrox():
    #x_new = 5.0
    global poly_yarr
    global poly_xarr
    poly_yarr = PolyAprox(xarr,yarr)
    poly_xarr = xarr
    #with dpg.stage(tag="Stage2"):
    #    dpg.add_line_series(x=[xarr[0],x_new],y=[yarr[0],y_appr], tag="Approx")
    #dpg.move_item(item="Approx", parent="Graph")

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
    

def BtnCreateTable():
    with dpg.window(tag="Primary Window1", width=600, height=800):
        with dpg.table(header_row=True, pos=(20, 400), height=200, width=500, tag="Table", show=True):
            dpg.add_table_column(label="X")
            dpg.add_table_column(label="Y")
            dpg.add_table_column(label="Z")
            for i in range(0, 30):
                with dpg.table_row(height=10):
                    for j in range(0,3):
                        dpg.add_input_double(step=0, step_fast=0)

dpg.create_context()
imageWidth_bCreate, imageHeight_bCreate, imageChannels_bCreate, imageData_bCreate = dpg.load_image("icons/table_create.png")
imageWidth_bImport, imageHeight_bImport, imageChannels_bImport, imageData_bImport = dpg.load_image("icons/import.png")
#"https://www.flaticon.com/free-icons/import" Import icons created by surang - Flaticon</a>
imageWidth_bSaveTable, imageHeight_bSaveTable, imageChannels_bSaveTable, imageData_bSaveTable = dpg.load_image("icons/floppy-disk.png")
imageWidth_bDraw, imageHeight_bDraw, imageChannels_bDraw, imageData_bDraw = dpg.load_image("icons/CreateGraph.png")
imageWidth_bApprox, imageHeight_bApprox, imageChannels_bApprox, imageData_bApprox = dpg.load_image("icons/Approximator.png")
#"https://www.flaticon.com/free-icons/save" Save icons created by tastyicon - Flaticon</a>
imageWidth_bSaveGraph, imageHeight_bSaveGraph, imageChannels_bSaveGraph, imageData_bSaveGraph = dpg.load_image("icons/SaveGraph.png")
with dpg.texture_registry():
    dpg.add_static_texture(width=imageWidth_bCreate, height=imageHeight_bCreate, default_value=imageData_bCreate, tag="imageCreate")
    dpg.add_static_texture(width=imageWidth_bImport, height=imageHeight_bImport, default_value=imageData_bImport, tag="imageImport")
    dpg.add_static_texture(width=imageWidth_bSaveTable, height=imageHeight_bSaveTable, default_value=imageData_bSaveTable, tag="imageSaveTable")
    dpg.add_static_texture(width=imageWidth_bDraw, height=imageHeight_bDraw, default_value=imageData_bDraw, tag="imageDraw")
    dpg.add_static_texture(width=imageWidth_bApprox, height=imageHeight_bApprox, default_value=imageData_bApprox, tag="imageApprox")
    dpg.add_static_texture(width=imageWidth_bSaveGraph, height=imageHeight_bSaveGraph, default_value=imageData_bSaveGraph, tag="imageSaveGraph")
with dpg.font_registry():
    with dpg.font("fonts/notomono-regular.ttf", 20, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font("Default font")

with dpg.file_dialog(directory_selector=False, show=False, callback=file_select_callback, file_count=1, id="file_dialog_id", width=800 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension("Source files (*.csv){.csv}", color=(0, 255, 255, 255))


with dpg.window(tag="Primary Window", width=800, height=600):
    with dpg.tab_bar(tag ="Tab_bar"):
        with dpg.tab(label="Модель 1", tag="Tab1"):
            with dpg.group(horizontal=True, tag="GroupBtn"):
                dpg.add_image_button(texture_tag="imageCreate", width=50, height=50, tag="TableCreate", callback=BtnCreateTable), SetTooltip("Создать таблицу")
                dpg.add_image_button(texture_tag="imageImport", width=50, height=50, callback=lambda: dpg.show_item("file_dialog_id")), SetTooltip("Загрузить таблицу")
                dpg.add_image_button(texture_tag="imageSaveTable", width=50, height=50), SetTooltip("Сохранить таблицу")
                dpg.add_image_button(texture_tag="imageDraw", width=50, height=50, callback=BtnDrawGraph), SetTooltip("Нарисовать график")
                dpg.add_image_button(texture_tag="imageApprox", width=50, height=50, callback=BtnAprrox), SetTooltip("Аппроксимировать")
                dpg.add_image_button(texture_tag="imageSaveGraph", width=50, height=50), SetTooltip("Сохранить график")
            with dpg.drawlist(width=800, height=600, tag="drawlist"):
                dpg.draw_rectangle(pmin=[400.0, 0.0], pmax=[780.0, 300.0], color=[0, 0, 0, 255], thickness=1)
                dpg.draw_rectangle(pmin=[400.0, 300.0], pmax=[780.0, 600.0], color=[0, 0, 0, 255], thickness=1)
                dpg.draw_line(p1=[0, 0], p2=[400, 0], color=[0, 0, 0])
                dpg.draw_line(p1=[0, 0], p2=[0, 600], color=[0, 0, 0])
                dpg.draw_line(p1=[0, 599], p2=[400,599], color=[0, 0, 0])
                dpg.draw_line(p1=[400, 440], p2=[780, 440], color=[0, 0, 0])
            with dpg.group(horizontal=True, pos=[410,400], before="drawlist"):
                dpg.add_text("Соединить:")
                dpg.add_combo(items=["Линия", "Сплайн"], width=100, default_value="Линия")
            with dpg.group(horizontal=True, pos=[410,450], before="drawlist"):
                dpg.add_text("Цвет соединения:")
                dpg.add_color_edit(default_value=[0, 0, 0], no_inputs=True)
            with dpg.group(horizontal=True, pos=[410,500], before="drawlist"):
                dpg.add_text("Толщина:")
                dpg.add_combo(items=["0,5 pt", "1 pt", "2 pt", "4 pt", "6 pt"], default_value="1 pt", width=80)
            dpg.add_text("Интервал осей:", pos=[410, 605])
            with dpg.group(horizontal=False, pos=[550, 570], before="drawlist"):
                dpg.add_text("По оси X:")
                dpg.add_spacer(width=10)
                dpg.add_text("По оси Y:")
                dpg.add_spacer(width=10)
                dpg.add_text("По оси Z:")
            with dpg.group(horizontal=False, pos=[640, 570], width=100, before="drawlist"):
                dpg.add_input_intx(size=2)
                dpg.add_spacer(width=10)
                dpg.add_input_intx(size=2)
                dpg.add_spacer(width=10)
                dpg.add_input_intx(size=2)
            with dpg.group(horizontal=False, pos=[415,100], before="drawlist"):
                dpg.add_text("Выберите метод аппроксимации:")
                dpg.add_combo(["Экспоненциальный", "Полиноминальный"], default_value="Полиноминальный", width=250)
                dpg.add_text("Выберите степень полинома \nдля аппроксимации:")
                dpg.add_input_int(tag= "poly_num", width=100)

with dpg.theme() as container_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 230, 230))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (180, 180, 180))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (180, 180, 180))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Header, (180,180,180))

dpg.bind_theme(container_theme)
dpg.create_viewport(title='Model App', width=808, height=750)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()