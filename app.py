# app.py
from flask import Flask, request, jsonify, url_for, send_file
app = Flask(__name__)

from gtts import gTTS
import requests
import json
import os
from pathlib import Path

# calls 15.ai model
def callPony(text, character):

  headers = {
      'authority': 'api.15.ai',
      'access-control-allow-origin': '*',
      'accept': 'application/json, text/plain, */*',
      'sec-ch-ua-mobile': '?0',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
      'sec-ch-ua-platform': '"Windows"',
      'content-type': 'application/json;charset=UTF-8',
      'origin': 'https://15.ai',
      'sec-fetch-site': 'same-site',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://15.ai/',
      'accept-language': 'en-US,en;q=0.9',
  }

  data = '{"text":"' + text + '","character":"' + character + '","emotion":"Contextual"}'
  
  
  response = requests.post('https://api.15.ai/app/getAudioFile5', headers=headers, data=data)
  
  
  wavName = json.loads(response.text)['wavNames'][0] # like nQJFDSJJKAFS.wav
  
  
  headers = {
      'authority': 'cdn.15.ai',
      'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
      'sec-ch-ua-platform': '"Windows"',
      'accept': '*/*',
      'origin': 'https://15.ai',
      'sec-fetch-site': 'same-site',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://15.ai/',
      'accept-language': 'en-US,en;q=0.9',
  }
  
  url = 'https://cdn.15.ai/audio/' + wavName
  return url
  '''
  with requests.get(url, headers=headers, stream=True) as r:
      r.raise_for_status()
      with open(wavName, 'wb') as f:
          for chunk in r.iter_content(chunk_size=8192): 
              # If you have chunk encoded response uncomment if
              # and set chunk_size parameter to None.
              #if chunk: 
              f.write(chunk)
  return wavName
  '''
  
  
@app.route('/data/<path:filename>', methods=['GET', 'POST'])
def getData(filename):
    Path("data").mkdir(parents=True, exist_ok=True)
    return send_file('data/' + filename)

@app.route('/gtts', methods=['GET'])
def get_gtts():
    Path("data").mkdir(parents=True, exist_ok=True)
    text = request.args.get('text', None)
    filename = 'gtts-' + text + ".mp3"
    outfile = "data/" + filename
    if not os.path.isfile(outfile):
        tts = gTTS(text=text)
        tts.save(outfile)
    return str(request.base_url).replace("gtts", "") + outfile
    
@app.route('/15ai', methods=['GET'])
def get_15ai():
    try:
        char = request.args.get("character", None)
        text = request.args.get('text', None)
        filename = callPony(text, char)
        return filename
    except Exception as e:
        return "Contact Phylliida to fix server\nError:\n" + str(e)
    
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
