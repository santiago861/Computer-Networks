from flask import Flask,jsonify,request
import requests
from getmac import get_mac_address
import time

app = Flask(__name__)
name = 'Santiago'
mac = get_mac_address()
initial_variable = 0


next_node= 'https://05a0-2806-2f0-91a0-bda0-3faa-68a8-87cf-a09.ngrok-free.app'

def send_message(variable):
    json = {

        'variable': variable,
        'name': name,
        'mac': mac
    }
    response = requests.post(f'{next_node}/receive_variable', json=json)
    if response.status_code != 200:
         print(f'Algo ha salido mal', response.status_code)


@app.route('/start_process',methods = ['GET'])
def start_process():
    global initial_variable
    send_message(initial_variable)
    return jsonify({'message' : 'mensaje enviado', 'variable': initial_variable})


@app.route('/receive_variable',methods = ['POST'])
def receive_variable():
    data = request.json
    variable = data.get('variable')
    if variable is not None:
        print(f'recibi la variable {variable}')
        variable +=1
        if variable >=50:
            print(f'Proceso finalizado por:", {name}')
            return jsonify({"valor": variable, "final_person": name})
        else:
            time.sleep(1)
            send_message(variable)
            return jsonify({"message": "Variable actualizada y enviada", "variable": variable})
    return jsonify({"error": "Invalid data"}), 400


app.run(port = 5002)