from . import feature_extractions as fnc
import pickle

def predict_url(url):
    data_url = fnc.predict_url_type(url)

    file_name = "model.pkl"
    model_ = pickle.load(open(file_name, 'rb'))

    output = model_.predict(data_url)[0]
    return str(output)
