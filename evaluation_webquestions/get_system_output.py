import requests
import json
import sys
import time

qa_url = 'http://139.91.183.96:5001/answer'
output_file = 'system_output.json'
time_output = 'get_system_output_time.json'

dataset = []
with open('webquestions_test_converted.json', encoding='utf8') as json_file:
    # 100 questions
    dataset = json.load(json_file)[0:100]

    # all questions (2039)
    #dataset = json.load(json_file)
try:
    with open(output_file, encoding='utf8') as json_file:
        answered = json.load(json_file)
    with open(time_output, encoding='utf8') as timeJson_file:
        answered_times = json.load(timeJson_file)
except FileNotFoundError:
    answered = []
    answered_times = []

answered_ids = []
for q in answered_times:
    if "Total time" not in q:
        answered_ids.append(int(q["id"]))
    else:
        del q

qcounter = len(dataset)
acounter = len(answered_ids)
total_time = 0
print('remaining: '+str(qcounter-acounter)+' questions')
for q in dataset:
    # start timer
    start = time.time()
    if(q["id"] in answered_ids):  # or q["id"] in {18,71,77}):
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
    # end timer
    end = time.time()
    q_time = end - start
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
    answered_times.append({
        "id": q["id"],
        "time":  q_time
    })
    with open(time_output, 'w') as outTime:
        json.dump(answered_times, outTime)

for ans in answered_times:
    total_time += ans['time']
answered_times.append({
    "Total time":  total_time
})
with open(time_output, 'w') as outTime:
    json.dump(answered_times, outTime)
