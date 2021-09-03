import requests
import json

def load_secrets(f):
        return json.load(f)

def run(args):
    secrets = load_secrets(args.secrets)
    base_url = 'https://api.edap-cluster.com/useeio/api'
    #Now use the endpoint to return a list of available models
    headers = {}
    headers['x-api-key']=secrets["apiKey"]
    models_response = requests.get(base_url+'/models',headers=headers)
    models = models_response.json()
    print(models[0])
    #Returns output like
    #[{'id': 'USEEIOv1.1',
    #  'name': 'USEEIOv1.1',
    #  'location': 'US',
    #  'description': 'EPA national life cycle model of goods and services, v1.1.'}]
