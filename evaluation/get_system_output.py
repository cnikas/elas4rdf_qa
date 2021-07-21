import requests
import json
import sys
import time

qa_url = 'http://139.91.183.96:5001/answer'
output_file = 'system_output.json'

dataset = []
with open('webquestions_test_converted.json', encoding='utf8') as json_file:
    # 100 questions
    # dataset = json.load(json_file)[0:100]

    # all questions (2039)
    dataset = json.load(json_file)
try:
    with open(output_file, encoding='utf8') as json_file:
        answered = json.load(json_file)
except FileNotFoundError:
    answered = []

answered_ids = []
for q in answered:
    answered_ids.append(int(q["id"]))

qcounter = len(dataset)
acounter = len(answered_ids)
print('remaining: '+str(qcounter-acounter)+' questions')
for q in dataset:
    # start timer
    start = time.time()
    if(q["id"] in answered_ids):
        continue
    else:
        print(q["id"])
    print(q['question'])
    payload = {
        'question': q['question'],
    }
    r = requests.get(qa_url, params=payload)
    try:
        response = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        sys.exit(1)
    response["id"] = q["id"]
    response["question"] = q["question"]
    # remove unwanted info
    response.pop("category")
    response.pop("types")
    for ans in response["answers"]:
        ans.pop("text")
        ans.pop("entity")
    # if "text" in response
    answered.append(response)
    # print(response)
    with open(output_file, 'w') as outfile:
        json.dump(answered, outfile)
