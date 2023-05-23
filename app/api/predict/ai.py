from . import feature_extractions as fnc
from ..pihole.update_list import add_domain
import pickle

def predict_url(url):
    data_url = fnc.predict_url_type(url)

    file_name = "model.pkl"
    model_ = pickle.load(open(file_name, 'rb'))

    output = model_.predict(data_url)[0]
    
    if output == 0:
        add_domain(url, "regex_white")
    else:
        add_domain(url, "regex_black")
    
    return str(output)
