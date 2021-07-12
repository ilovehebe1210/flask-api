# -*- coding:UTF-8 -*-

from app import app

import pickle

pickle_in = open(r'apps/model/randomforest.pickle', 'rb')
forest = pickle.load(pickle_in)

def predict(input):
    pred = forest.predict(input)[0]
    print(pred)
    return pred



@app.route('/')
def index():
    return 'Flask API started'



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)
