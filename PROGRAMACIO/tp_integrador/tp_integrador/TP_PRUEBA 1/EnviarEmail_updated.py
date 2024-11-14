# Importación de las bibliotecas necesarias
import requests  # requests permite realizar peticiones HTTP (en este caso, a la API de EmailJS)
import json  # json se utiliza para convertir los datos de Python a formato JSON

# Configuración de los datos necesarios para enviar un correo electrónico usando la API de EmailJS
data = {
    'service_id': 'service_tq6wwwh',  # ID del servicio en EmailJS
    'template_id': 'template_mx23lgn',  # ID de la plantilla de correo en EmailJS
    'user_id': 'kPneVDwcNx4UK_xyp',  # ID de usuario en EmailJS
    'accessToken': 'vs9nufahysZPpyZwuUS9L',  # Token de acceso para autenticar la solicitud
    'template_params': {  # Parámetros específicos para la plantilla de correo
        'from_name': 'Tobias',  # Nombre del remitente del correo
        'to_name': '{}',  # Nombre del destinatario (se puede personalizar)
        'message': 'Cotizacion pedida {}'  # Mensaje personalizado (se puede personalizar con datos adicionales)
    }
}

# Configuración de los encabezados HTTP para la solicitud
headers = {
    'Content-Type': 'application/json',  # Especifica que el contenido es JSON
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',  # Simula un navegador en la solicitud
    'Accept': 'application/json, text/javascript, */*; q=0.01',  # Especifica los tipos de contenido aceptados en la respuesta
    'Accept-Language': 'en-US,en;q=0.9',  # Especifica el idioma preferido para la respuesta
    'Origin': 'http://127.0.0.1:5000',  # Define la URL de origen desde la que se envía la solicitud
    'Referer': 'http://127.0.0.1:5000/'  # URL de referencia, generalmente la página desde la cual se hace la solicitud
}

# Intenta enviar el correo electrónico mediante una solicitud POST
try:
    response = requests.post(
        'https://api.emailjs.com/api/v1.0/email/send',  # URL de la API de EmailJS para enviar correos
        data=json.dumps(data),  # Convierte el diccionario `data` a JSON para enviarlo en el cuerpo de la solicitud
        headers=headers  # Incluye los encabezados HTTP configurados
    )
    response.raise_for_status()  # Lanza una excepción si la respuesta HTTP indica un error
    print('Your mail is sent!')  # Imprime un mensaje si el correo se envía con éxito
    print('Status Code:', response.status_code)  # Imprime el código de estado de la respuesta
    print('Response:', response.text)  # Imprime el contenido de la respuesta

# Maneja las excepciones que puedan ocurrir al realizar la solicitud HTTP
except requests.exceptions.RequestException as error:
    print(f'Oops... {error}')  # Imprime el error ocurrido
    if error.response is not None:
        print(error.response.text)  # Si hay una respuesta de error, imprime el texto de la respuesta