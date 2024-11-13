import joblib
from flask import Flask, render_template, request


crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('home.html')  

# Prediction form route
@app.route('/Predict')
def prediction():
    return render_template('Index.html')

# Form submission and prediction route
@app.route('/form', methods=["POST"])
def brain():
    try:
        # Get form inputs
        Nitrogen = float(request.form['Nitrogen'])
        Phosphorus = float(request.form['Phosphorus'])
        Potassium = float(request.form['Potassium'])
        Temperature = float(request.form['Temperature'])
        Humidity = float(request.form['Humidity'])
        Ph = float(request.form['ph'])
        Rainfall = float(request.form['Rainfall'])

        # Validate inputs to ensure they're positive and within realistic ranges
        if Nitrogen <= 0 or Phosphorus <= 0 or Potassium <= 0 or Temperature <= 0 or Humidity <= 0 or Ph <= 0 or Rainfall <= 0:
            return "Error: All values must be positive."

        if not (0 <= Ph <= 14 and 0 <= Temperature <= 100 and 0 <= Humidity <= 100):
            return "Error: Please enter realistic values for temperature, humidity, and pH."

        # Prepare the input values
        values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

        # Load the trained model
        model = joblib.load('crop_app')  # Ensure your model file 'crop_app' is in the correct location

        # Make prediction
        prediction_id = model.predict([values])[0]  # Assuming model outputs a single prediction ID
        
        # Get the corresponding crop name from the dictionary
        prediction_crop = crop_dict.get(prediction_id, "Unknown Crop")

        # Render the prediction result in the template
        return render_template('prediction.html', prediction=prediction_crop)

    except FileNotFoundError:
        return "Model file not found. Please ensure that the model file 'crop_app' exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, port=7000)

