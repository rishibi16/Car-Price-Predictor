from flask import Flask, render_template, request
import jsonify
import requests
import joblib
import numpy as np
import sklearn
import datetime

app = Flask(__name__)
model = joblib.load('car_price_predictor.pkl')
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        myDict = request.form
        Year = int(myDict['Year'])
        Present_Price = float(myDict['Present_Price'])
        Kms_Driven = int(myDict['Kms_Driven'])
        Owner = int(myDict['Owner'])
        Fuel_Type_Petrol = myDict['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == "Petrol"):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == "Diesel"):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0
        now = datetime.datetime.now()
        Year = now.year - Year
        Seller_Type_Individual = myDict['Seller_Type_Individual']
        if(Seller_Type_Individual == "Individual"):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = myDict['Transmission_Manual']
        if(Transmission_Manual == 'Manual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        
        predict = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        final = round(predict[0], 2)
        if final < 0:
            return render_template('index.html', ans = "Sorry you cannot sell this car")
        else:
            return render_template('index.html', ans = "You Can Sell The Car at {} lac.".format(final))
    else:
        return render_template('index.html') 
if __name__ == "__main__":
    app.run(debug=True)            
