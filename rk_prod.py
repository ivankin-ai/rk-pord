from flask import Flask, session, send_file, request, render_template
from werkzeug.datastructures import ImmutableMultiDict

import config
import main

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
def index():
    # TODO: Index.html
    #   1. Создать базу
    #   2. Сделать Модальное окно и его автоподгрузку
    return render_template('index.html')


@app.route("/test", methods=['POST', 'GET'])
def input_atr():
    atr_dict = config.atr_dict
    if request.method == "POST":
        atr = {
            'method_fixing': request.form['method_fixing'],
            'type_template': request.form['type_template'],
            'size_a': int(request.form['size_a']),
            'size_b': int(request.form['size_b']),
            'dist': int(request.form['dist']),
            'ind_diam': int(request.form['ind_diam']),
            'ind_num': int(request.form['ind_num']),
        }

        # Мб сделать с помощью обработки словаря:
        # imd = request.form
        # imd.to_dict(flat=False)
        # for k, v in imd.items():
        #     print(k, v, ': ', type(v))

        name = main.name_file(atr)
        if main.check_file(name):
            return send_file('files/pdf/' + main.name_file(atr) + '.pdf', as_attachment=True)
        main.create_dxf(atr)
        file = main.DXF2IMG()
        file.convert_dxf2img('Files/DXF/', name)
        return send_file('files/pdf/' + main.name_file(atr) + '.pdf', as_attachment=True)
    return render_template('create.html', atr_dict=atr_dict)


# Отображает три карточки: конус / полоса / парковка + модальные окна к иникаторам
@app.route("/template", methods=['POST', 'GET'])
def select_template():
    templates = [
        {'name': 'Конус',
         'href': '#',
         'description': 'Здесь должно быть описание',
         'img': {'src': 'static/images/templates/cone.png', 'alt': 'Конус'},
         'idModal': 'coneModal'},
        {'name': 'Полоса',
         'href': '#',
         'description': 'Здесь должно быть описание',
         'img': {'src': 'static/images/templates/strip.png', 'alt': 'Полоса'},
         'idModal': 'stripModal'},
        {'name': 'Парковка',
         'href': 'template/parking',
         'description': 'Здесь должно быть описание',
         'img': {'src': 'static/images/templates/parking.png', 'alt': 'Парковка'}}
    ]

    # TODO: трафареты
    #   Сделать модальные окна для каждого из трафаретов кроме пакрковки
    return render_template('template.html', templates=templates)


#  Формыа для создания трафаретов в зависимости от выбраного модального окна (их примерно 6)
@app.route("/template/editor", methods=['POST', 'GET'])
def edit_template():
    # TODO:
    #   сделать создание трафаретов с выплывающим модальным окном, с автоподгрузкой:
    #       расчёта, эскиза, кнопкой скачивания, и добавлением в избраное
    pass


# Карточки трафаретов Парковки из ПЭТ 0,7мм
@app.route("/template/parking")
def parking():

    templates = [
        {
            'id': 1,
            'name': 'Трафарет парковка 1600х800мм',
            'description': '''
            Здесь должно быть описание трафарета. 
            Трафарет для разметки места для инвалидов.
            Изготовлен из ПЭТ 0,7мм
            Блаблаблаблаблаблаблаблаблабла.
            блаблаблаблаблаблаблаблаблабла
            блаблаблаблаблаблабла
            ''',
            'png': {
                'path': '/static/files/png/Трафарет парковка 1600х800.png'
            },
            'pdf': {
                'path': '/static/files/pdf/Трафарет парковка 1600х800.pdf'
            },
            'dxf': {
                'path': '/static/files/dxf/Трафарет парковка 1600х800.dxf'
            },
            'price': 5640,
            'rating': 1
        },
        {
            'id': 2,
            'name': 'Трафарет парковка 1600х800мм',
            'description': '''
            Здесь должно быть описание трафарета. 
            Трафарет для разметки места для инвалидов.
            Изготовлен из ПЭТ 0,7мм
            Блаблаблаблаблаблаблаблаблабла.
            блаблаблаблаблаблаблаблаблабла
            блаблаблаблаблаблабла
            ''',
            'png': {
                'path': '/static/files/png/Трафарет парковка 800х800.png'
            },
            'pdf': {
                'path': '/static/files/pdf/Трафарет парковка 800х800.pdf'
            },
            'dxf': {
                'path': '/static/files/dxf/Трафарет парковка 800х800.dxf'
            },
            'price': 550,
            'rating': 2
        },
        {
            'id': 3,
            'name': 'Трафарет парковка 1600х800мм',
            'description': '''
            Здесь должно быть описание трафарета. 
            Трафарет для разметки места для инвалидов.
            Изготовлен из ПЭТ 0,7мм
            Блаблаблаблаблаблаблаблаблабла.
            блаблаблаблаблаблаблаблаблабла
            блаблаблаблаблаблабла
            ''',
            'png': {
                'path': '/static/files/png/Трафарет парковка 1200х800.png'
            },
            'pdf': {
                'path': '/static/files/pdf/Трафарет парковка 1200х800.pdf'
            },
            'dxf': {
                'path': '/static/files/dxf/Трафарет парковка 1200х800.dxf'
            },
            'price': 870,
            'rating': 4
        }
    ]

    # TODO: Parking.html
    #   0. Создать БД для трафаретов
    #   1. Сделать подгрузку из БД готовых трафаретов
    #   2. Отредактировать шаблон для трафаретов парковки
    #   3. Сделать модальное окно с подробным описанием каждого из трафаретов

    return render_template('parking.html', templates=templates)


# Мои заказы


# @app.route("/create", method=['POST', 'GET'])
# def select_type():
#     type = {
#         'Конус. Линейый порядок': 'Л',
#         'Конус. Шахматный порядок': 'Ш',
#         'Полоса. Путь': 'П_П',
#         'Полоса. Поле получения услуги': 'П_У',
#     }
#     if request.method == "POST":
#         method_fixing = request.form['method_fixing']
#         # GOTO: Сделать выбор метода крепления
#         if method_fixing == 'Приклеивание':
#             pass
#         elif method_fixing == 'Сверление':
#             pass
#         else:
#             return 404
#         type_input = {
#
#         }
#         pass
#     return render_template('select_type.html')


if __name__ == '__main__':
    app.run(debug=True)


