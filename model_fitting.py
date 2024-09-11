import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_excel(
    'files/dataset/chatgpt-gen-extended_synthetic_leakage_current_earthing_data.xlsx')

def predict_condition(row):
    leakage_current = row['Leakage Current (mA)']
    humidity = row['Humidity (%)']
    temperature = row['Temperature (C)']
    earth_resistance = row['Earth Resistance (Ohms)']

    if leakage_current > 3 or (humidity > 70 and temperature > 40) or earth_resistance > 150:
        return "danger"
    elif leakage_current > 1.5:
        return "warning (leakage)"
    elif humidity > 60:
        return "warning (humidity)"
    elif earth_resistance > 100:
        return "warning (earth resistance)"
    else:
        return "good"


df['Predicted Condition'] = df.apply(predict_condition, axis=1)
df.to_excel(
    'files/dataset/updated_dataset_with_extended_conditions.xlsx', index=False)
print("Updated dataset saved as 'updated_dataset_with_extended_conditions.xlsx'.")


'''
Danger: High leakage current (>3 mA) or a combination of high humidity (>70%) and high temperature (>40°C).
Warning (leakage): Medium leakage current (>1.5 mA).
Warning (humidity): High humidity (>60%).
Good: None of the above conditions are met.
Earth Resistance Warning: Earth resistance greater than 100 ohms leads to a "warning (earth resistance)".
Ground Potential Rise Warning: Ground potential rise greater than 10 V triggers a "warning (ground potential rise)".
'''


df = pd.read_excel(
    'files/dataset/updated_dataset_with_extended_conditions.xlsx')
label_encoder = LabelEncoder()
df['Predicted Condition'] = label_encoder.fit_transform(
    df['Predicted Condition'])
X = df[['Leakage Current (mA)', 'Earth Resistance (Ohms)', 'Humidity (%)',
        'Temperature (C)']]
y = df['Predicted Condition']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

with open('leakage_condition_model.pkl', 'wb') as model_file:
    pickle.dump(clf, model_file)

with open('label_encoder.pkl', 'wb') as le_file:
    pickle.dump(label_encoder, le_file)
