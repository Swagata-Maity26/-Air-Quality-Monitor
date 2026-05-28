from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "ce121353fa43106b7b75e336b9f1fd87219e3bc7"

@app.route("/", methods=["GET","POST"])
def home():

    city=""
    aqi=None
    status=""
    advice=""

    if request.method=="POST":

        city=request.form["city"]

        url=f"https://api.waqi.info/feed/{city}/?token={API_KEY}"

        response=requests.get(url)
        data=response.json()

        if data["status"]=="ok":

            aqi=data["data"]["aqi"]

            if aqi<=50:
                status="Good 😊"
                advice="Air quality is good. Outdoor activities are fine."

            elif aqi<=100:
                status="Moderate 😐"
                advice="Sensitive people should reduce long outdoor exposure."

            elif aqi<=150:
                status="Unhealthy"
                advice="Children and older adults should limit outdoor activity."

            elif aqi<=200:
                status="Poor 😷"
                advice="Wear a mask and avoid heavy exercise outside."

            else:
                status="Hazardous ☠️"
                advice="Stay indoors as much as possible."

        else:
            status="City not found"

    return render_template(
        "index.html",
        city=city,
        aqi=aqi,
        status=status,
        advice=advice
    )

if __name__=="__main__":
    app.run(debug=True)