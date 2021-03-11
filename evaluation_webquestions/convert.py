"""
This script is used to convert the webquestions dataset to a format that is
easy to use with the other scripts.
"""
import json
import re

with open("webquestions.test.json",encoding="utf8") as json_file:
    data = json.load(json_file)

    
def clean_answers(tv):
    clean = []
    matches = re.findall('(?<=description ).*?(?=\))', tv)
    for m in matches:
        clean.append(m.replace("\"",""))
    return clean
    
output = []

id = 1
for q in data:
    current = {
        "id": id,
        "question": q["utterance"],
        "answers": clean_answers(q["targetValue"])
    }
    output.append(current)
    
with open('webquestions_test_converted.json', 'w') as outfile:
    json.dump(output, outfile)