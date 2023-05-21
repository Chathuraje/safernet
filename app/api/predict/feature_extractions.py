import socket
import whois
import pandas as pd
from sklearn import preprocessing
import geocoder
import re


def __get_ip_address(domain):
    try:
        ip = socket.gethostbyname(domain)
        # Convert IP address to numerical representation
        ip = sum(int(digit) * (256 ** i) for i, digit in enumerate(ip.split('.')[::-1]))
        return ip
    except socket.gaierror:
        return 0


def __get_geo_location(domain):
    try:
        ip = socket.gethostbyname(domain)
        g = geocoder.ip(ip)
        if g and g.country:
            country_name = g.country

            label_encoder = preprocessing.LabelEncoder()
            country_name = label_encoder.fit_transform([country_name])[0]
            return country_name
        else:
            return 0
    except socket.gaierror:
        return 0


def __get_tld_from_domain(domain):
    # Extracting top-level domain
    tld = domain.split(".")[-1]
    label_encoder = preprocessing.LabelEncoder()
    tld = label_encoder.fit_transform([str(tld)])[0]  # Convert tld to string

    return tld

def __get_whois(domain):
    try:
        whois_data = whois.whois(domain)
        return whois_data
    except Exception as e:
        return None

def __is_whois_complete(domain):
    whois_data = __get_whois(domain)
    REQUIRED_WHOIS_FIELDS = ['domain_name', 'registrar', 'registrant_name', 'creation_date', 'expiration_date']
    
    if whois_data is None:
        return 0

    for field in REQUIRED_WHOIS_FIELDS:
        if field not in whois_data:
            return 0

    return 1

# Finding https_status
import http.client
def __check_https(url):
  https_status= 0
  
  try:
    conn = http.client.HTTPSConnection(url)
    conn.request("HEAD", "/")
    res = conn.getresponse()
    if res.status == 200 or res.status==301 or res.status==302:
        https_status= 1   
  
  except Exception as msg:
    https_status= 0
    
  finally:
    return https_status

def __count_features(domain):
  features = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '*', '//']
  data = []

  for feature in features:
    data.append(domain.count(feature))

  return data

def __digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def __letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def __shorting(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0
    
    
def __generate_info(domain):
    ip_add = __get_ip_address(domain)
    geo_loc = __get_geo_location(domain)
    tld = __get_tld_from_domain(domain)
    who_is = __is_whois_complete(domain)
    https = __check_https(domain)
    features = __count_features(domain)
    digits = __digit_count(domain)
    letters = __letter_count(domain)
    sh_services = __shorting(domain)

    return [ip_add, geo_loc, tld, who_is, https, features, digits, letters, sh_services]


def predict_url_type(url):
    data = __generate_info(url)

    flattened_data = []
    for item in data:
        if isinstance(item, list):
            flattened_data.extend(item)
        else:
            flattened_data.append(item)

    column_names = ['ip_add', 'geo_loc', 'tld', 'who_is', 'https', '@', '?', '-', '=', '.', '#', '%', '+', '$', '*', '//', 'digits', 'letters', 'shortings']
    df = pd.DataFrame([flattened_data], columns=column_names)

    return df