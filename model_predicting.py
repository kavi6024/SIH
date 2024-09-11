import pickle

import warnings
warnings.filterwarnings("ignore")


# Load the model
with open('leakage_condition_model.pkl', 'rb') as model_file:
    clf = pickle.load(model_file)

# Load the label encoder
with open('label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)


def predictor(arr):
    true_labels = [
        'Leakage Current (mA)', 'Earth Resistance (Ohms)', 'Humidity (%)', 'Temperature (C)']
    predictions = clf.predict(arr)
    predicted_conditions = label_encoder.inverse_transform(predictions)
    print(predicted_conditions[0])
