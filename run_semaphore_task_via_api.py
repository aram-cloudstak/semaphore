import requests
import json

# Semaphore API base URL
base_url = 'http://localhost:3000/api'

# Login to Semaphore and get a user token
login_url = f'{base_url}/auth/login'
login_data = {
    'auth': 'admin',
    'password': 'Hyper10n'
}

response = requests.post(login_url, json=login_data, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
if response.status_code != 204:
    print('Login failed!')
    exit()
print('Login successful.')

# Save cookies to use in subsequent requests
cookies = response.cookies



# Get user tokens
tokens_url = f'{base_url}/user/tokens'
response = requests.get(tokens_url, cookies=cookies)

if response.status_code != 200:
    print('Failed to retrieve user tokens!')
    exit()
print('List tokens successful.')

tokens = response.json()

# Check if tokens exist, and if not, generate a new token
if not tokens:
    print('No token found. Getting new token.')
    generate_token_url = f'{base_url}/user/tokens'
    response = requests.post(generate_token_url, cookies=cookies, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    
    if response.status_code != 200:
        print('Failed to generate a new token!')
        exit()

    tokens = response.json()

# Extract the token ID
token_id = tokens[0]['id']
print('New token aquired.'+token_id)

# Use the token as a bearer token in the header for subsequent requests
headers = {
    'Authorization': f'Bearer {token_id}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}



# Run a task
run_task_url = f'{base_url}/project/2/tasks'

# Note: API gives a 400 error when trying to use the bool values below. Need to troubleshoot that.
task_data = {
    'template_id': 1,
#    'debug': true,
#    'dry_run': false,
#    'diff': false,
#    'playbook': '',
#    'environment': {}
}

response = requests.post(run_task_url, json=task_data, headers=headers)

if response.status_code != 201:
    print('Failed to run the task! HTTP error ' + str(response.status_code))
else:
    print('Task submitted successfully.')
    print(f'Status Code: {response.status_code}')

response_data = response.json()
print('Response Data:')
print(json.dumps(response_data, indent=4))


print('Done.')
