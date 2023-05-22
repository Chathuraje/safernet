import os
from dotenv import load_dotenv
import configparser

load_dotenv()

config = configparser.ConfigParser()
config.read('config.ini')

url=config.get('PIHOLE', 'PIHOLE_IP')

PIHOLE_API_URL = f"http://{url}/admin/api.php"
PIHOLE_API_KEY = os.getenv("PI_HOLE_API_KEY") 
