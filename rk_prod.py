from flask import Flask, session, send_file, request, render_template
from werkzeug.datastructures import ImmutableMultiDict

import config
import main

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def hello() -> str:
#     atr = config.atr
#     return send_file('files/pdf/' + main.name_file(atr) + '.pdf')


@app.route("/", methods=['POST', 'GET'])
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
            return send_file('files/pdf/' + main.name_file(atr) + '.pdf')
        main.create_dxf(atr)
        file = main.DXF2IMG()
        file.convert_dxf2img('Files/DXF/', name)
        return send_file('files/pdf/' + main.name_file(atr) + '.pdf')
    return render_template('create.html', atr_dict=atr_dict)


app.secret_key = config.SECRET_KEY


if __name__ == '__main__':
    app.run(debug=True)


