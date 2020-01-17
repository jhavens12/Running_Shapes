import webbrowser
import json
import requests
import credentials


def main():
    # STEP 1:
    auth_url = 'www.strava.com/oauth/authorize?client_id='+credentials.client_id+'&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all'
    print()
    print(auth_url)
    #webbrowser.open('googlechrome://'+auth_url)  # Go to example.com
    print()
    full_url = input("What is the full URL? ")

    #cut out the url code from the full url for ease
    cut1 = full_url.split('=',2)
    cut2 = cut1[2].split('&',1)
    url_code = cut2[0]

    # STEP 2: (Take code from step one URL and put in "CODE section below" then look for Access Token in response)

    url = 'https://www.strava.com/api/v3/oauth/token'
    data = {
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'code': url_code,
      'grant_type': 'authorization_code'
    }

    response = requests.post(url, data=data).json()
    print()
    print(response['access_token'])
    print(response['access_token'],  file=open('./api_key.txt', 'w'))

    print()
    print("DONE")

    return response['access_token']
