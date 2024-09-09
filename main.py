from flask import Flask, render_template, request, jsonify
import email_handler

app = Flask(__name__)

# Sample data for dropdown options (could come from a database or your CSV file)
dropdown_options = {
    "leakage_current": [0.1, 5.0, 10.0, 20.0, 50.0],
    "earth_resistance": [10, 50, 100, 500, 1000],
    "temperature": [15, 25, 35, 45, 50],
    "humidity": [20, 50, 80, 100],
    "voltage": [110, 220, 240],
    "continuity_status": [0, 1],
    "phase": ["A", "B", "C", "Neutral"]
}

# Function to determine leakage condition based on leakage current
def evaluate_leakage_condition(leakage_current):
    if leakage_current <= 5:
        return "Good Condition"
    elif 5 < leakage_current <= 10:
        return "Warning: Must Monitor"
    else:
        return "Bad Condition: Must Treat Now"

@app.route('/')
def index():
    return render_template('index.html', options=dropdown_options)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    leakage_current = float(data.get('leakage_current', 0))
    
    # Determine condition based on leakage current
    condition = evaluate_leakage_condition(leakage_current)

    if condition in ["Warning: Must Monitor", "Bad Condition: Must Treat Now"]:
        email_handler.send_email(
            email_handler.decrypter("219880-217968-200760-204584-185464-225616-200760-214144-217968-200760-231352-185464-210320-97512-122368-196936-208408-185464-200760-206496-87952-189288-212232-208408"),
            email_handler.decrypter("196936-208408-185464-200760-206496-204584-185464-225616-200760-122368-103248-91776-95600-99424"),
            "srikavipriyan3@gmail.com",
            condition,
            email_handler.create_html_representation(data)
        )
        print("Email sent")
    
    # Return data and condition
    return jsonify({"condition": condition})

if __name__ == '__main__':
    app.run(debug=True)
