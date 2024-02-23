# import libraries
from flask import Flask, jsonify, request
from tensorflow import keras
import numpy as np
import json
import phishing_features


# Creating Flask app
app = Flask(__name__)

# Loading pre-trained keras model
def loadModel():
    path = "models48xLSTM-32xDense"
    model = keras.models.load_model(path)
    return model

model = loadModel()

# Make prediction using loaded keras model
def make_predict(url):
    x_predict = phishing_features.featureExtraction(url)
    print(x_predict, " - Extracted features")
    x_predict = np.array(x_predict)
    x_predict = np.reshape(x_predict, (1, 1, x_predict.shape[0])) # Ensure correct shape for prediction
    prediction = model.predict(x_predict)
    print(prediction[0], " - Predicted value before thresholding")
    return thresholding(prediction[0])

# Thresholding function
def thresholding(prediction):
    threshold = 0.8
    if prediction > threshold:
        return 1
    else:
        return 0

# Routing for POST requests
@app.route("/", methods=['GET', 'POST'])
def index():
    if (request.method == "POST"):
        response = request.get_json()
        predict = make_predict(response["url"])
        print(predict, "- predicted value")
        # Modify the response to include the prediction result
        response_data = {
            "prediction": predict
        }
        return jsonify(response_data)
    else:
        print("Error - Not received POST method")
        return jsonify({"state":-1})

if __name__ == "__main__":
    app.run(debug=True)
