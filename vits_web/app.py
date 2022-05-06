import os

from flask import Flask, request, render_template, send_file
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def index():
    return render_template("index.html", data="hey")

@app.route('/prediction', methods=["POST"])
def prediction():
    message = request.form['text']

    os.system(f'python ./TTS/TTS/bin/synthesize.py --text "{message}" \
      --model_path ./VITS_finetuned/vits_BSC_Gerard_Sant/best_model.pth \
      --config_path ./VITS_finetuned/vits_BSC_Gerard_Sant/config.json \
      --speaker_id my_speaker \
      --out_path ./VITS_finetuned/vits_web/output.wav')

    path_to_file = "output.wav"

    return send_file(
        path_to_file, 
        mimetype="audio/wav", 
        as_attachment=True, 
        attachment_filename="output.wav")

if __name__ == "__main__":
    app.run()