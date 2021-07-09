import pickle

pickle_in = open(r'apps/model/randomforest.pickle', 'rb')
forest = pickle.load(pickle_in)


def predict(input):
    pred = forest.predict(input)[0]
    print(pred)
    return pred
