import os
from flask import Flask, render_template, request
from werkzeug import secure_filename



from os import path
from pydub import AudioSegment
import os
from  pyAudioAnalysis.audioAnalysis import featureExtractionFileWrapper
import pandas as pd


from joblib import dump, load
import joblib
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression


__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'audio_files/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)


    file_location = 'audio_files'
    if ".mp3" in filename:
        sound = AudioSegment.from_mp3(os.path.join(file_location,filename))
        filename_no_extn=os.path.splitext(filename)[0]
        print(filename_no_extn)
        wav_filepath = os.path.join(file_location,filename_no_extn)+".wav"
        sound.export(wav_filepath, format="wav")
        featureExtractionFileWrapper(wav_filepath, 'audio_files/' + filename_no_extn + '_out', 1.0, 1.0, 0.050, 0.050 )

        feature_filepath = os.path.join('audio_files', filename_no_extn + '_out.csv')
        df = pd.read_csv(feature_filepath, header=None)

        features = []
        for col in df.columns:
            features.append(df[col].mean())
            features.append(df[col].min())
            features.append(df[col].max())
        feature_df = pd.DataFrame([features])
        predicted_gender = audio_gender_model.predict(feature_df)[0]
        return predicted_gender

        return render_template("complete.html", pred = predicted_gender)
        pred

    #return render_template('pass.html', n= name, age= age, db= db)
filename = os.path.join("D:/finalized", "finalized_model.sav")
audio_gender_model = joblib.load(filename)










if __name__ == "__main__":
    app.run(port=4555, debug=True)
