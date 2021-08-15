from pprint import pprint
import requests


user_id = '' # id открытого профиля
token = '' # token ВК
params ={'user_id': user_id,
		'fields':'bdate',
		'access_token': token,
		'v':'5.131'
		}
response = requests.get('https://api.vk.com/method/friends.get', params=params)



if response.ok:
	j_data = response.json()
	data = j_data.get('response').get('items')
	with open("out_file.txt", "a", encoding='utf-8') as out_f:
		for i in data:
			out_f.write(f"{i.get('first_name')} {i.get('last_name')} {i.get('bdate')}"+"\n")

	
		