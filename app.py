from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

API_KEY = "e097f522a8804b6cdeb81527f3e58637"

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/style.css")
def style():
    return send_from_directory('.', 'style.css')

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": data.get("message", "API error")}), response.status_code

    weather_info = {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "main": data["weather"][0]["main"]
    }
    return jsonify(weather_info)

if __name__ == "__main__":
    app.run(debug=True)
