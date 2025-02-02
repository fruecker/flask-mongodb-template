import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        ip_address = data['ip']
        return ip_address
    except requests.RequestException:
        return None