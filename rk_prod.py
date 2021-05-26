from flask import Flask, session, send_file, request, render_template
from werkzeug.datastructures import ImmutableMultiDict

import config
import main

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route("/", methods=['POST', 'GET'])
def index():
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


