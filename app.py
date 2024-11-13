import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')  


@app.route('/Predict')
def prediction():
    return render_template('Index.html')

@app.route('/Predict Your Crop')
def add():
    return render_template('form.html')

@app.route('/form', methods=["POST"])
def brain():
    try:
        # Get the form data
        Nitrogen = float(request.form['Nitrogen'])
        Phosphorus = float(request.form['Phosphorus'])
        Potassium = float(request.form['Potassium'])
        Temperature = float(request.form['Temperature'])
        Humidity = float(request.form['Humidity'])
        Ph = float(request.form['ph'])
        Rainfall = float(request.form['Rainfall'])
        
        # Values list for prediction
        values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

        # Validate input
        if not (0 < Ph <= 14):
            return render_template('error.html', message="Invalid pH value. It should be between 0 and 14.")
        if not (Temperature < 100):
            return render_template('error.html', message="Temperature should be less than 100°C.")
        if not (Humidity > 0):
            return render_template('error.html', message="Humidity should be greater than 0.")
        
        # Crop dictionary mapping
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }

        # If model is loaded correctly, predict
        import joblib
        model = joblib.load('crop_app')
        if model:
            arr = [values]
            prediction = model.predict(arr)

            # Map the predicted index to the crop name
            crop_index = int(prediction[0])  # Assuming the model returns an integer index for the crop
            predicted_crop = crop_dict.get(crop_index, "Unknown crop")

            return render_template('prediction.html', prediction=predicted_crop)
        else:
            return render_template('error.html', message="Model file not found. Please ensure the model is available.")
    
    except Exception as e:
        # Handle any other errors, such as invalid data type or missing fields
        return render_template('error.html', message=f"Error processing the form: {str(e)}")

if __name__ == '__main__':
        app.run(debug=True, port=7000)
