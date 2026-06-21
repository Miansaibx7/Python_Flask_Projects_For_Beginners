from flask import Flask,render_template,request
from datetime import datetime
import requests

app = Flask(__name__)

API_KEY = your_api_key

@app.route('/', methods=['POST','GET'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
              url =f" https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
              response = requests.get(url)
              if response.status_code == 200:
                  data = response.json()
                  weather_data = {
                      'city' : city,
                      'temperature': data['main']['temp'],
                      'humidity' : data ['main'] ['humidity'],
                      'description' : data['weather'][0]['description'],
                      'datetime' : datetime.now().strftime('%Y-%m-%d "%I:%M %p"')
                  }
              else:
                error = "City not found or API error."
        else:
            error = "Please enter a city name."

    return render_template('base.html', weather=weather_data, error=error)

if __name__ =="__main__":
    app.run(debug=True)
                
