import joblib
from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('app.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

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
        
        # Log the form data
        logger.info(f"Received form data: Nitrogen={Nitrogen}, Phosphorus={Phosphorus}, Potassium={Potassium}, "
                    f"Temperature={Temperature}, Humidity={Humidity}, Ph={Ph}, Rainfall={Rainfall}")

        # Values list for prediction
        values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, Ph, Rainfall]

        # Validate input
        if not (0 < Ph <= 14):
            logger.error("Invalid pH value. It should be between 0 and 14.")
            return render_template('error.html', message="Invalid pH value. It should be between 0 and 14.")
        
        if not (Temperature < 100):
            logger.error("Temperature should be less than 100°C.")
            return render_template('error.html', message="Temperature should be less than 100°C.")
        
        if not (Humidity > 0):
            logger.error("Humidity should be greater than 0.")
            return render_template('error.html', message="Humidity should be greater than 0.")
        
        # Crop dictionary mapping
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }

        # Load the model and predict
        try:
            model = joblib.load('crop_app')
            if model:
                arr = [values]
                prediction = model.predict(arr)

                # Map the predicted index to the crop name
                crop_index = int(prediction[0])  # Assuming the model returns an integer index for the crop
                predicted_crop = crop_dict.get(crop_index, "Unknown crop")

                logger.info(f"Predicted crop: {predicted_crop}")
                return render_template('prediction.html', prediction=predicted_crop)
            else:
                logger.error("Model file not found. Please ensure the model is available.")
                return render_template('error.html', message="Model file not found. Please ensure the model is available.")
        except Exception as e:
            logger.error(f"Error loading the model: {str(e)}")
            return render_template('error.html', message=f"Error loading the model: {str(e)}")

    except Exception as e:
        # Handle other errors, such as invalid data type or missing fields
        logger.error(f"Error processing the form: {str(e)}")
        return render_template('error.html', message=f"Error processing the form: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=7000)


