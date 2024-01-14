# app.py
from flask import Flask, render_template, jsonify,request
from flask_caching import Cache
import requests
from StocksData import getWebData, screenCandle
from datetime import datetime, timedelta



app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_data', methods=['POST'])
def process_data():
    print("Inside Process data")
    data_from_js = request.get_json('data')
    
    ## process data
    selectedSector = data_from_js.get('selectedSector')
    selectedCandlePattern = data_from_js.get('selectedCandlePattern')
    webData = getData(selectedSector=selectedSector)    

    result = screenCandle(webData,selectedCandlePattern)
    
    return jsonify({'result': result})

@cache.cached(timeout=3600, key_prefix='custom_cache_key')
def getData(selectedSector):
    webData = getWebData(selectedSector=selectedSector)
    #print(webData,type(webData))
    return webData

if __name__ == '__main__':
    app.run(debug=True)
