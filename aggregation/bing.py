import requests
import secrets
import csv
import json
import time

search_terms = []#["trayvon martin"] #"ahmaud arbery"]
'''

WAPO_CSV = 'wapo-data.csv'

with open(WAPO_CSV) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader) #get rid of first row (labels)
    for row in csv_reader:
        name = row[1].lower()
        search_terms.append(name)

with open('search terms.txt', 'w+') as f:
    for term in search_terms:
        print(term, file=f)
'''
with open('search terms.txt') as f:
    for line in f:
        search_terms.append(line)

subscription_key = secrets.subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
max_count = 100

count_mapping = {}
i = 0
for search_term in search_terms:
    i += 1
    print(f"trying {search_term} - ", i)
    time.sleep(1.5)
    params  = {"q": search_term}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    total_number = search_results['totalEstimatedMatches']
    count_mapping[search_term] = total_number

    '''
    for i in range(int(total_number / max_count)):
        print(f"made {i}th request of {total_number / max_count} for {search_term}")
        params  = {"q": search_term, "count": 100, 'offset': i*max_count}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        for result in search_results['value']:
            cache.append((result['name'], result['provider'][0]['name'], result['datePublished']))
    with open(search_term+'.news.search', 'w+') as f:
        for line in cache:
            print(line, file=f)   
    '''    
with open("count_mapping.json", "w+") as f:
    print(json.dumps(count_mapping), file=f)



