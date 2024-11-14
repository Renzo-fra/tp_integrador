from flask import Flask, jsonify, request 
import requests
import json
from datetime import datetime,timedelta
from flask_cors import CORS 

app = Flask(__name__) 
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}}) 

cotizaciones = []
def obtener_cotizaciones():
    api_url = "https://dolarapi.com/v1/dolares"
    response = requests.get(api_url) 
    datos_api = response.json() 

    for cotizacion in datos_api:
        nombre = cotizacion.get("nombre", "Desconocido")
        tipo = cotizacion.get("casa", "Desconocido")
        compra = cotizacion.get("compra")
        venta = cotizacion.get("venta")
        fecha = cotizacion.get("fechaActualizacion")

        cotizaciones.append({ 
            "nombre": nombre,
            "tipo": tipo,
            "compra": compra,
            "venta": venta,
            "fecha": fecha
        })
    
    return cotizaciones 

@app.route("/api/cotizaciones", methods=["GET"]) 
def api_cotizaciones():
    return jsonify(obtener_cotizaciones()) 

@app.route('/api/contacto/', methods=['POST', 'OPTIONS'])
def contacto():
    if request.method == 'OPTIONS':
        response = app.response_class(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400
    mail_enviar(data['nombre'],data['apellido'],'tobianfuso@gmail.com',data['mensaje'])
    return jsonify({"status": "Contacto recibido", "data": data}), 200

def mail_enviar(nombre,apellido,email,informacion_enviar):
    data = {
        'service_id': 'service_tq6wwwh',
        'template_id': 'template_mx23lgn',
        'user_id': 'kPneVDwcNx4UK_xyp',
        'accessToken': 'vs9nufahysZPpyZwuUS9L',
        'template_params': {
            'from_name': 'Pagina Cotizaciones',
            'to_name': f'{nombre} {apellido}',
            'to_mail':f'{email}',
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
    
@app.route('/api/historico/<tipo_dolar>/<fecha_inicio>/<fecha_fin>/<int:valores>', methods=["GET"])
def api_historico(tipo_dolar, fecha_inicio, fecha_fin, valores):
    api_url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{tipo_dolar}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        datos = response.json()
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

if __name__ == "__main__":
    app.run(debug=True) 