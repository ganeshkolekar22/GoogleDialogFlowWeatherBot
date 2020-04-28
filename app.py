import json
import os
import requests
from flask import Flask #microframework to develope web qpp
from flask import request
from flask import make_response

app=Flask(__name__)
# app route decorator. when webhook is called, the decorator would call the functions which are e defined

@app.route('/webhook', methods=['POST'])
def webhook():
    #convert data from json
    req = request.get_json(silent=True, force=True)

    # extract the relevant information and use api and get the response and send it dialogflow.
    # helper function
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    user_says = result.get('queryText')
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    # day = parameters.get('forday')
    # date = parameters.get("date")
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+',in&appid=db91df44baf43361cbf73026ce5156cb')
    json_object=r.json()
    allParam = json_object['list'][0]
    date = allParam['dt_txt']
    main = allParam['main']
    kelvinTemp = main['temp']
    celsiusTemp = kelvinTemp - 273.15
    humidity = main['humidity']
    pressure = main['pressure']
    desc = allParam['weather'][0]['description']
    day1 = date.split(" ")[0]
    speech = ("Today's Forcast: \n date- "+day1+" \ntemp: "+str(celsiusTemp)+" \nhumidity: "+str(humidity)+" \npressure: "+str(pressure)+" \ndescription: "+desc)
    return {
        "fulfillmentText": speech
    }
    # return {
    # "speech": speech,
    # "displayText":speech,
    # "source":"apiai-weather-webhook"}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 1000))
    print("starting on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

