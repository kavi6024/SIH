import requests
from bs4 import BeautifulSoup
import time
import model_predicting


def extract_float(value):
    number = ''.join(c for c in value if (c.isdigit() or c == '.'))
    return float(number)


url = 'http://192.168.137.187/'
while True:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        strong_tags = soup.find_all('strong')
        data = {}
        for tag in strong_tags:
            key = tag.get_text(strip=True)
            value = tag.find_next_sibling(string=True).strip()
            data[key] = value
        
        leakage_current = extract_float(data['Leakage Current (Analog):'])
        earth_resistance = extract_float(data['Earth resistance (Analog):'])
        humidity = extract_float(data['Humidity:'])
        temperature = extract_float(data['Temperature:'])
        model_predicting.predictor([[leakage_current, earth_resistance, humidity, temperature]])

    else:
        print(f"Cannot access site, status code : {response.status_code}")
        break
    time.sleep(0.5)
