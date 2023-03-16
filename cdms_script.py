
import requests

host = 'https://npt-cdms.nezperce.org/services/api/v1/'
username = 'api_user'
password = 'api_user'
login = 'account/login'
data = {'username':username, 'password':password}
s = requests.Session()
auth = s.post(url = host+login, data = data)


year = 2021
dataset = 4334
reddurl = 'https://npt-cdms.nezperce.org/services/api/v1/npt/getsgsredddata'
params = {'SurveyYear':year, 'DatasetID':dataset}
req = s.get(url = reddurl, params = {'SurveyYear':year, 'DatasetID':dataset})
print(req.status_code)
print(req.json())

# import pandas as pd
# import json
# df = pd.json_normalize(req.json())




spp = 'Chinook'
#url = 'npt/getfinsweirdata'
url = 'npt/getjuvabundancedata'
params = {'Species':spp}
# req = requests.get(url = host+url)
req = s.get(url = host+url)
print(req.status_code)
print(req.json())