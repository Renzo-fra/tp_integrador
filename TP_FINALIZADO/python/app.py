from flask import Flask, jsonify, request 
import requests
import json
from datetime import datetime,timedelta
from flask_cors import CORS 

class CotizacionesAPI:
    def __init__(self):
        self.api_url = "https://dolarapi.com/v1/dolares"
    def obtener_datos_api(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except requests.exception.RequestExepcion as e:
            print(f"error al obtener la cotizacion de la api: {e}")
        return[]

class Cotizaciones:
    def __init__(self, api_client):
        self.api_client = api_client

    def obtener_cotizaciones(self):
        datos_api = self.api_client.obtener_datos_api()

        cotizaciones = []

        for cotizacion in datos_api:
            cotizaciones.append({
                "nombre": cotizacion.get("nombre"),
                "tipo": cotizacion.get("casa"),
                "compra": cotizacion.get("compra"),
                "venta": cotizacion.get("venta"),
                "fecha": cotizacion.get("fechaActualizacion"),
            })
        return cotizaciones

app = Flask(__name__)
CORS (app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

cotizaciones_api = CotizacionesAPI()
cotizaciones_service = Cotizaciones(cotizaciones_api)

@app.route("/api/cotizaciones", methods=["GET"])
def api_cotizaciones():
    return jsonify(cotizaciones_service.obtener_cotizaciones())




@app.route('/api/contacto/', methods=['POST', 'OPTIONS'])
def contacto():
    if request.method == 'OPTIONS':
        # Responde a la solicitud preflight con un estado 200 y headers de CORS
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Procesa la solicitud POST aquí
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    # Aca podes agregar el procesamiento que necesites con data, como guardar en una base de datos o enviar un correo
    mail_enviar(data['nombre'],data['apellido'],'tobianfuso@gmail.com',data['mensaje'],data['email'])
    return jsonify({"status": "Contacto recibido", "data": data}), 200

def mail_enviar(nombre,apellido,email,informacion_enviar,respuesta='tobiasanfuso@gmail.com'):
    data = {
        'service_id': 'service_tq6wwwh',
        'template_id': 'template_mx23lgn',
        'user_id': 'kPneVDwcNx4UK_xyp',
        'accessToken': 'vs9nufahysZPpyZwuUS9L',
        'template_params': {
            'from_name': 'Pagina Cotizaciones',
            'to_name': f'{nombre} {apellido}',
            'to_mail':f'{email}',
            'reply_to':f'{respuesta}',
            'message': f'Cotizacion pedida {informacion_enviar}'
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'application/json, text/javascript, /; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://your-website.com',  
        'Referer': 'https://your-website.com/'
    }

    try:
        response = requests.post(
            'https://api.emailjs.com/api/v1.0/email/send',
            data=json.dumps(data),
            headers=headers
        )
        response.raise_for_status()
        print('Your mail is sent!')
    except requests.exceptions.RequestException as error:
        print(f'Oops... {error}')
        if error.response is not None:
            print(error.response.text)
    
# Endpoint para datos históricos
@app.route('/api/historico/<tipo_dolar>/<fecha_inicio>/<fecha_fin>/<int:valores>', methods=["GET"])
def api_historico(tipo_dolar, fecha_inicio, fecha_fin, valores):
    api_url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{tipo_dolar}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        datos = response.json()
        #print(datos)
        fechas=[]
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        diferencia_fechas=(fecha_fin-fecha_inicio)/(valores-1)
        for cont in range(valores):
            fecha_str = (fecha_inicio+diferencia_fechas*cont).strftime("%Y-%m-%d")
            fechas.append(fecha_str)

        datos_historicos = []
        for fecha in fechas:
            for dato in datos:
                if(dato['fecha']==fecha):
                    datos_historicos.append({
                        'fecha':dato['fecha'],
                        'valor':dato['compra']
                    })
        print(datos_historicos)
        return jsonify(datos_historicos)

    except requests.exceptions.RequestException as e:
        print("Error al obtener datos de la API externa:", e)
        return jsonify({"error": "No se pudieron obtener los datos"}), 500




@app.route('/api/enviarCotizacion/', methods=['POST', 'OPTIONS'])
def obtener_enviar_cotizaciones():
    if request.method == 'OPTIONS':
        # Responde a la solicitud preflight con un estado 200 y headers de CORS
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    # Procesa la solicitud POST aquí
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    cotizaciones = cotizaciones_service.obtener_cotizaciones()
    print(data)

    email_cotizacion="cotizacion de dolares\n"
    for i in cotizaciones:
            email_cotizacion += f"{i['nombre']}\n"
            email_cotizacion += f"{i['tipo']}\n"
            email_cotizacion += f"{i['compra']}\n"
            email_cotizacion += f"{i['venta']}\n"
            email_cotizacion += f"{i['fecha']}\n"

    print(email_cotizacion)

    mail_enviar(data['nombre'],data['apellido'],data['email'], email_cotizacion)
    return jsonify({"status": "cotizacion recibida", "data": data}), 200




#inicia el servidor
if __name__ == "__main__":
    app.run(debug=True) 