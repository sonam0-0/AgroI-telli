from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import sklearn
import pickle
from sklearn.preprocessing import StandardScaler, MinMaxScaler



model = pickle.load(open('mode.pkl','rb'))
sc = pickle.load(open('standscale.pkl','rb'))
mx = pickle.load(open('minmaxscale.pkl','rb'))


dtr = pickle.load(open('dtr.pkl','rb'))
preprocessor = pickle.load(open('preprocessor.pkl','rb'))


crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

app = Flask(__name__)
def clean_input_data(features):
    """Clean the input data by stripping whitespace characters (spaces, tabs, etc.)"""
    return [[str(val).strip() for val in row] for row in features]


# Home route
@app.route('/')
def index():
    return render_template('home.html')  

@app.route('/login')
def login():
    return render_template('login.html') 

# Prediction form route
@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/prediction')
def prediction():
    return render_template('Index.html')

@app.route('/prediction2')
def prediction2():
    return render_template('main.html')


@app.route('/work',methods=['POST'])
def pred():
    if request.method=='POST':
        Year=request.form['Year']
        average_rain_fall_mm_per_year=request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = request.form['pesticides_tonnes']
        avg_temp = request.form['avg_temp']
        Area = request.form['Area']
        Item  = request.form['Item']
        # Load preprocessing pipeline
        

        
        features = np.array([[Year,average_rain_fall_mm_per_year,pesticides_tonnes,avg_temp,Area,Item]],dtype=object)
        
        cleaned_features = clean_input_data(features)
        transformed_features = preprocessor.transform(cleaned_features)
        prediction = dtr.predict(transformed_features).reshape(1,-1)
        predicted_yield = prediction[0] 
        return render_template('pro.html',prediction = predicted_yield)

# Form submission and prediction route
@app.route('/form', methods=["POST"])
def brain():
    try:
    
        N = int(request.form['Nitrogen'])
        P = int(request.form['Phosphorus'])
        K = int(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['Rainfall'])
    
    
        input_data = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], 
                          columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
    
        features_scaled = mx.transform(input_data )  
        features_scaled = sc.transform(features_scaled )  

        predicted_label = model.predict(features_scaled)[0]  

    # predicted_crop = {v: k for k, v in crop_dict.items()}[predicted_label]
        predicted_crop = crop_dict[predicted_label]

        # print(f"The recommended crop based on the input data is: {predicted_crop}")
        return render_template('prediction.html', result=predicted_crop)
     
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('prediction.html', result="An error occurred while making the prediction. Please check your input values.")

  


        
          

if __name__ == '__main__':
    app.run(debug=True, port=5000)

