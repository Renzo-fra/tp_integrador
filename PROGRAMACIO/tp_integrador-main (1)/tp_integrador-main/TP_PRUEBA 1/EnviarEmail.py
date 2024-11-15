import requests
import json                                        

data = {
    'service_id': 'service_tq6wwwh',
    'template_id': 'template_mx23lgn',
    'user_id': 'kPneVDwcNx4UK_xyp',
    'accessToken': 'vs9nufahysZPpyZwuUS9L',
    'template_params': {
        'from_name': 'Tobias',
        'to_name': '{}',
        'message': 'Cotizacion pedida {}'
    }
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
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