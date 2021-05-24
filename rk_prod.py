from flask import Flask, session, send_file, request, render_template
import config, main

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def hello() -> str:
#     atr = config.atr
#     return send_file('files/pdf/' + main.name_file(atr) + '.pdf')


@app.route("/", methods=['POST', 'GET'])
def register():
    atr_list = config.atr_list
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
        print(atr)
        name = main.name_file(atr)
        if main.check_file(name):
            return send_file('files/pdf/' + main.name_file(atr) + '.pdf')
        main.create_dxf(atr)
        file = main.DXF2IMG()
        file.convert_dxf2img('Files/DXF/', name)
        return send_file('files/pdf/' + main.name_file(atr) + '.pdf')
    return render_template('create.html', atr_list=atr_list)


# @app.route('/download', methods=['GET', 'POST'])
# def hello() -> str:
#     atr = config.atr
#     return send_file('files/pdf/' + main.name_file(atr) + '.pdf')


app.secret_key = config.SECRET_KEY


if __name__ == '__main__':
    app.run(debug=True)


