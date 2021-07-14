import requests
import json
import sys
import time

qa_url = 'http://139.91.183.96:5001/answer'
elas4rdf_url = 'https://demos.isl.ics.forth.gr/elas4rdf/entities_json'
output_file = 'system_output.json'
output_entity = 'entity_output.json'
total_time = 0


def getEntity(query, id):
    payload = {
        'query': query,
        'size': 1000
    }
    r = requests.get(elas4rdf_url, params=payload)
    try:
        response = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        sys.exit(1)
    response['results']['id'] = id
    response['results']['query'] = query
    for e in response['results']['entities']:
        e.pop('ext')
        e.pop('gain')
    return response['results']


def getQA(query, id):
    payload = {
        'question': query,
    }
    r = requests.get(qa_url, params=payload)
    try:
        response = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        sys.exit(1)
    response["id"] = id
    response["query"] = query

    # remove unwanted info
    response.pop("category")
    response.pop("types")
    for ans in response["answers"]:
        ans.pop("text")
    return response


def readQueries(filename):
    dataset = []
    with open(filename, encoding='utf8') as q:
        lines = q.readlines()
        for line in lines:
            tokens = line.replace('\n', '').split('\t')
            id = tokens[0]
            query = tokens[1]
            if "QALD2" in id:
                dataset.append({"id": id, "query": query})
    return dataset


try:
    with open(output_file, encoding='utf8') as json_file:
        qa_answered = json.load(json_file)
    with open(output_entity, encoding='utf8') as json_file:
        en_answered = json.load(json_file)
except FileNotFoundError:
    qa_answered = []
    en_answered = []

qa_dataset = readQueries('queries-v2.txt')
en_dataset = readQueries('queries-v2_stopped.txt')

assert(len(qa_dataset) == 140 and len(en_dataset) == 140)

answered_ids = []
for q in qa_answered:
    answered_ids.append(q["id"])

qcounter = len(qa_dataset)
acounter = len(answered_ids)
print('remaining: '+str(qcounter-acounter)+' queries')
for qa, en in zip(qa_dataset, en_dataset):
    if(qa["id"] in answered_ids):
        continue
    print(qa["id"], qa['query'])
    response_qa = getQA(qa['query'], qa['id'])
    response_entity = getEntity(en['query'], en['id'])
    qa_answered.append(response_qa)
    en_answered.append(response_entity)
    with open(output_file, 'w') as outfile:
        json.dump(qa_answered, outfile)
    with open(output_entity, 'w') as outfile:
        json.dump(en_answered, outfile)
