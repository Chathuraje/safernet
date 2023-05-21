import boto3
from botocore.exceptions import NoCredentialsError

def __get_digital_ocean_file():
    access_key = 'DO00G398EW9K9PH3NLNJ'
    secret_key = 'cvx8hVYEF659K8BuZZCFekk3Cj+MJjS4sUn7fR3rgMU'
    bucket_name = 'safernet-model'
    remote_file_path = 'model.pkl'
    local_file_path = 'app/api/predict'

    session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_client = session.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com')

    try:
        s3_client.download_file(bucket_name, remote_file_path, local_file_path)
        print('Model file downloaded successfully.')
    except NoCredentialsError:
        print('Error: Could not access DigitalOcean Spaces. Check your credentials.')
    except Exception as e:
        print(f'Error: {e}')
        
        
__get_digital_ocean_file()