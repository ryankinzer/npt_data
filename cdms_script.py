
import requests

username = 'api_user'
password = 'api_user'
url = 'https://npt-cdms.nezperce.org/services/api/v1/account/login'
data = {'username':username, 'password':password}

s = requests.Session()
r = s.post(url = url, data = data)


year = 2021
dataset = 4334
reddurl = 'https://npt-cdms.nezperce.org/services/api/v1/npt/getsgsredddata'
params = {'SurveyYear':year, 'DatasetID':dataset}
req = requests.get(url = reddurl, params = {'SurveyYear':year, 'DatasetID':dataset})
print(req.status_code)
print(req.json())

import pandas as pd
import json
df = pd.json_normalize(req.json())