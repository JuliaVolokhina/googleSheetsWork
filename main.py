!pip install numpy==1.16.1
import pandas as pd
import numpy as np
import keras
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
import pickle

import os
from flask import Flask

app = Flask(__name__)

df = pd.read_excel('dataset3new.xlsx', header=None, names=['inputname', 'schoolname']).astype(str)
num_classes = len(df['schoolname'].drop_duplicates())
X = df['inputname'].values
Y = df['schoolname'].values

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = load_model('schoolModel.h5')
#classes = { 'МАОУ "Гимназия № 108"': 0, 'МАОУ "Гимназия № 3"': 1, 'МАОУ "Гимназия № 31"': 2, 'МАОУ "Гимназия № 4"': 3, 'МАОУ "Гимназия № 87"': 4, 'МАОУ "Лицей  № 62"': 5, 'МАОУ "Лицей "Солярис"': 6, 'МАОУ "Лицей математики и информатики"': 7, 'МАОУ "Лицей № 3 им. А.С. Пушкина"': 8, 'МАОУ "Лицей № 36"':9, 'МАОУ "Лицей № 37"':10,'МАОУ "Медико-биологический лицей"': 11, 'МАОУ "СОШ "Аврора"': 12, 'МАОУ "СОШ № 21 им. П.А. Столыпина"': 13, 'МАОУ "Физико-технический лицей № 1"': 14, 'МБОУ "Гимназия № 8" г. Энгельс': 15, 'МБОУ "Лицей № 15"': 16, 'МБОУ "ООШ № 104"': 17, 'МБОУ "ООШ № 91"': 18, 'МБОУ "СОШ № 16"': 19, 'МБОУ "СОШ № 90"': 20, 'МОУ "Восточно-Европейский лицей"': 21, 'МОУ "Гимназия № 1"': 22, 'МОУ "Гимназия № 34"': 23, 'МОУ "Гимназия № 5"': 24, 'МОУ "Гимназия № 58"': 25, 'МОУ "Гимназия № 7"': 26, 'МОУ "Гимназия № 75 имени Д.М. Карбышева"': 27, 'МОУ "Гимназия № 89"': 28, 'МОУ "Гуманитарно-экономический лицей"': 29, 'МОУ "Лицей прикладных наук имени Д.И. Трубецкова"': 30, 'МОУ "Лицей № 107"':31, 'МОУ "Лицей № 2"':32, 'МОУ "Лицей № 4"':33, 'МОУ "Лицей № 47"':34, 'МОУ "Лицей № 50"':35, 'МОУ "Лицей № 53"':36, 'МОУ "Лицей № 56"':37, 'МОУ "Национальная (татарская) гимназия"': 38, 'МОУ "ООШ № 17"': 39, 'МОУ "ООШ № 26"': 40, 'МОУ "ООШ № 78"': 41, 'МОУ "ООШ № 81"': 42, 'МОУ "СОШ № 1"': 43, 'МОУ "СОШ № 10"': 44, 'МОУ "СОШ № 100"': 45, 'МОУ "СОШ № 101"': 46, 'МОУ "СОШ № 102"': 47, 'МОУ "СОШ № 103"': 48, 'МОУ "СОШ № 105"': 49, 'МОУ "СОШ № 106"': 50, 'МОУ "СОШ № 11"': 51, 'МОУ "СОШ № 18"': 52, 'МОУ "СОШ № 19" г. Энгельс': 53, 'МОУ "СОШ № 2 УИП им. В.П. Тихонова"': 54, 'МОУ "СОШ № 22"': 55, 'МОУ "СОШ № 23"': 56, 'МОУ "СОШ № 24"': 57, 'МОУ "СОШ № 28"': 58, 'МОУ "СОШ № 32" г. Энгельс': 59, 'МОУ "СОШ № 33" г. Энгельс': 60, 'МОУ "СОШ № 38"': 61, 'МОУ "СОШ № 39"': 62, 'МОУ "СОШ № 4" г. Энгельс': 63, 'МОУ "СОШ № 40"': 64, 'МОУ "СОШ № 41"': 65, 'МОУ "СОШ № 43 имени В.Ф. Маргелова"': 66, 'МОУ "СОШ № 44"':67, 'МОУ "СОШ № 45"':68, 'МОУ "СОШ № 46"':69, 'МОУ "СОШ № 48"':70, 'МОУ "СОШ № 49"': 71, 'МОУ "СОШ № 5 имени В. Хомяковой"': 72, 'МОУ "СОШ № 51"': 73, 'МОУ "СОШ № 52"': 74, 'МОУ "СОШ № 54"': 75, 'МОУ "СОШ № 55"': 76, 'МОУ "СОШ № 57"': 77, 'МОУ "СОШ № 59 с УИП"': 78, 'МОУ "СОШ № 6"': 79, 'МОУ "СОШ № 60"': 80, 'МОУ "СОШ № 61"': 81, 'МОУ "СОШ № 63"': 82, 'МОУ "СОШ № 64"': 83, 'МОУ "СОШ № 66 им. Н.И. Вавилова"': 84, 'МОУ "СОШ № 67 им. О.И. Янковского"': 85, 'МОУ "СОШ № 69"': 86, 'МОУ "СОШ № 7"': 87, 'МОУ "СОШ № 70"': 88, 'МОУ "СОШ № 71"': 89, 'МОУ "СОШ № 72"': 90, 'МОУ "СОШ № 73"': 91, 'МОУ "СОШ № 76"': 92, 'МОУ "СОШ № 77"': 93, 'МОУ "СОШ № 8"': 94, 'МОУ "СОШ № 82"': 95, 'МОУ "СОШ № 83"': 96, 'МОУ "СОШ № 84"': 97, 'МОУ "СОШ № 86"': 98, 'МОУ "СОШ № 9"': 99, 'МОУ "СОШ № 93"': 100, 'МОУ "СОШ № 94"': 101, 'МОУ "СОШ № 95 с УИОП"': 102, 'МОУ "СОШ № 97"': 103, 'МОУ "ООШ № 14"': 104,  'ЧОУ "Лицей-интернат естественных наук"': 105, 'ЧОУ "Лицей-интернат № 6 ОАО "РЖД"':106}

@app.route('/<text>')
def predict(text):
    encoder = LabelEncoder()
    encoder.classes_ = np.load('classes.npy')
    encoder.transform(Y)
    X_new = [text]
    #tokenizer.fit_on_texts(X)
    x_test = tokenizer.texts_to_matrix(X_new, mode='binary')
    prediction = model.predict(np.array(x_test))
    classnumber = np.argmax(prediction[0])
    return (', '.join(encoder.inverse_transform([classnumber])))


def main():
    if 'HEROKU' in os.environ:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()

if __name__ == '__main__':
    main()
