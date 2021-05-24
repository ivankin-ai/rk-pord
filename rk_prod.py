from flask import Flask, session, send_file
import config, main
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello() -> str:
    atr = config.atr
    return send_file('files/pdf/' + main.name_file(atr) + '.pdf')


app.secret_key = config.SECRET_KEY


if __name__ == '__main__':
    app.run(debug=True)


