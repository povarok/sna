import requests
import json
import csv
from datetime import datetime
from time import sleep

api_version = "5.5.2"

def write_json(data):
    with open('posts.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
 
def to_json(post_dict):
	try:
		data = json.load(open('posts_data.json'))
	except:
		data = []

	data.append(post_dict)
	
	with open('posts_data.json', 'w', encoding='utf8') as file:
		json.dump(data, file, indent=2, ensure_ascii=False)


def write_csv(data):
	with open('posts_data.csv', 'a', encoding='utf8') as file:
		writer = csv.writer(file)

		writer.writerow((data['likes'],
						 #data['reposts'],
						 data['text']
						 ))

def get_data(post):
	try:
		post_id = post ['id']
	except:
		post_id = 0
	try:
		likes = post['likes']['count']
	except:
		likes = 'zero'
	#try:
	#	reposts = post['reposts']['count']
	#except:
	#	reposts = 'zero'
	try:
		text = post['text']
	except:
		text = '***'
	data = {
		'id': post_id,
		'likes': likes,
	#	'posts': reposts,
		'text': text
	}
	return data




def main():
	start = datetime.now()

    #https://api.vk.com/method/newsfeed.get?user_id=210700286&v=5.52
	group_id = '-30666517'
	offset = 0
	date_x = 1494013156
  
	tokenzi = 'a4c7076135266607151e19d402e33f923d0134343052303bc6ab1c564ac3e187c17314c0ddf16ec56bf13'
	all_posts = []
	while True:
		sleep(1)
		r = requests.get('https://api.vk.com/method/wall.get', params={ 'access_token': tokenzi, 'owner_id': group_id, 'count': 100, 'offset':  offset, 'version': api_version})
    	
		posts = r.json()['response']
    
		all_posts.extend(posts)


		oldest_post_date =  posts[-1]['date']


		offset += 100
		#print(offset)

		if oldest_post_date < date_x:
			break

	data_posts = []

	for post in all_posts:
		post_data = get_data(post)
		#print(post_data)
		write_csv(post_data)





	end = datetime.now()

	total = end - start
	#print(len(all_posts))
	#print(str(total))
    #data = json.load(open('posts.json', encoding='utf8'))
    #print(len(data['response']))


if __name__ == '__main__':
    main()
