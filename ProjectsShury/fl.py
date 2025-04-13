from flask import Flask, render_template, request, jsonify
from bully import parse_print, parse_group
from threading import Thread
import json

app = Flask(__name__, template_folder='.')

@app.route("/")
def web():
    return render_template('templates/headmenu.html')

@app.route("/autho")
def data():
    return render_template('templates/authentification.html')

@app.route("/api/process_data", methods=['POST'])
def send_data():
    try:
        data = request.get_json()  # Получаем JSON из запроса
        id = data['id']
        hash = data['hash']
        phone = data['phone']
        with open('data.txt', 'w') as file:
            file.write(id+'\n'+hash+'\n'+phone)
        return jsonify({'message': 'Данные успешно получены и обработаны!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/op")
def openweb():
    return render_template('templates/open.html', parse_print=parse_print)

@app.route('/api/process_data1', methods=['GET', 'POST'])
def send_data1():
    try:
        data1 = request.get_json()
        number = data1['number_chat']
        with open('number.txt', 'w') as file:
            file.write(number)
        return jsonify({'message': 'Данные успешно получены и обработаны!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/process")
def process():
    return render_template("templates/processing.html", parse_group=parse_group)

@app.route("/bullyi")
def test_bully():
    return render_template("templates/bull.html")

if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0", port=85)


def keep_alive():
    t = Thread(target=__name__)
    t.start()