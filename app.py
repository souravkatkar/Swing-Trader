# app.py
from flask import Flask, render_template, jsonify,request
import requests
from StocksData import screenCandlePattern
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_data', methods=['POST'])
def process_data():
    print("Inside Process data")
    data_from_js = request.get_json('data')
    print(data_from_js)

    
    # Perform some processing on the data (e.g., a simple transformation)
    selectedSector = data_from_js['selectedSector']
    selectedCandlePattern = data_from_js['selectedCandlePattern']

    result = screenCandlePattern(selectedCandlePattern=selectedCandlePattern,selectedSector=selectedSector)
  

    # Return the processed data
    return jsonify({'result': result})



if __name__ == '__main__':
    app.run(debug=True)
