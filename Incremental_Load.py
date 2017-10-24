import requests
import json
import csv
import pandas as pd
from pandas.io.json import json_normalize
import pprint
import numpy as np
from flatten_json import flatten
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import math
from datetime import datetime, timedelta, date

YOUR_ACCESS_TOKEN = 'XXXXX'

df = pd.DataFrame()
df_Dedup = pd.DataFrame()
df_Append = pd.DataFrame()
df_Append1 = pd.DataFrame()
#survey_id = '115970747'

s = requests.session()

s.headers.update({
  "Authorization": "Bearer %s" % YOUR_ACCESS_TOKEN,
  "Content-Type": "application/json"
})

start_date = str(date.today() - timedelta(days=8))
days_to_subtract = 1
End_Date = str(date.today())
current_date = str(date.today())



for survey_id in ['XXXX'] :
#for survey_id in ['116267744'] :
	print survey_id
	k = 100
	url = "https://api.surveymonkey.net/v3/surveys/%s/responses/bulk" % (survey_id)
	payload_full = {'start_modified_at' : start_date , 'end_modified_at' : End_Date}
	r = s.get(url,params = payload_full)
	output = json.loads(r.content)
	total = output['total']
	print total
	page = int(math.ceil(total/100.0))
	Last_Page_Count = total - (page-1)*100
	print page
	print Last_Page_Count
	for p in np.arange(1,page+1,1):
		payload = {'page' : p , 'per_page' : k,'start_modified_at' : start_date , 'end_modified_at' : End_Date}
		r = s.get(url,params = payload)
		output = json.loads(r.content)
		if p == page:
			k=Last_Page_Count
		print k
		for i in np.arange(k):
			flat_json = [flatten(output['data'][i]) for row_id in output['data'][i]]
			df = pd.DataFrame(flat_json)
			del df['analyze_url']
			del df['collection_mode']
			del df['custom_value']
			del df['edit_url']
			del df['href']
			del df['recipient_id']
			df_Append = df_Append.append(df,ignore_index=True)


if 'page_path_0' in df_Append.columns:
	del df_Append['page_path_0']

if 'page_path_1' in df_Append.columns:
	del df_Append['page_path_1']

if 'page_path_2' in df_Append.columns:	
	del df_Append['page_path_2']


df_Append1 = df_Append.drop_duplicates()
df_Append1.to_csv('data.csv')

