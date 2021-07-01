import requests
import json
import sys
import time

qa_url = 'http://139.91.183.96:5001/answer'
output_file = 'system_output_entity.json'
total_time = 0
dataset = []
with open('qald2.txt', encoding='utf8') as q:
    lines = q.readlines()
    for line in lines:
        tokens = line.replace('\n', '').split('\t')
        id = tokens[0]
        query = tokens[1]
        dataset.append({"id": id, "query": query})
try:
    with open(output_file, encoding='utf8') as json_file:
        answered = json.load(json_file)
except FileNotFoundError:
    answered = []

answered_ids = []
for q in answered:
    total_time += float(q["time"])
    answered_ids.append(q["id"])

qcounter = len(dataset)
acounter = len(answered_ids)
print('remaining: '+str(qcounter-acounter)+' queries')
for q in dataset:
    if(q["id"] in answered_ids):
        continue
    print(q["id"], q['query'])
    payload = {
        'question': q['query'],
    }
    r = requests.get(qa_url, params=payload)
    try:
        response = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        sys.exit(1)
    response["id"] = q["id"]
    response["query"] = q["query"]
    total_time += response["time"]
    # remove unwanted info
    response.pop("category")
    response.pop("types")
    for ans in response["answers"]:
        ans.pop("text")

    answered.append(response)
    with open(output_file, 'w') as outfile:
        json.dump(answered, outfile)

print("\nTotal Time: "+str(total_time))
