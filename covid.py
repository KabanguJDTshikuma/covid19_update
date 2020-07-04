import requests
import json

api_key = "tgmPv_u_SvxQ"
project_token = "tWzFYYXqwnRF"

response = requests.get(f'https://www.parsehub.com/api/v2/projects/{project_token}/last_ready_run/data', params={"api_key": api_key})
data = json.loads(response.text)
print(data)