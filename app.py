import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
import json
import time

app = flask.Flask(__name__)
app.config['SECRET_KEY'] =  'e2b35432632f190f45201266'
print('Initializing...')
ae = AnswerExtraction()
atp = AnswerTypePrediction()
print('\tDONE')
 
@app.route('/answer', methods=['GET'])
def api_answer():
    args = request.args.to_dict()

    if 'question' in args:
        question = args['question']
    else:
        error_output = {'error':True}
        return jsonify(error_output)


    entities_json = json.loads(args['entities'])
    entities = [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in entities_json['results']['entities']]
    
    t1 = time.time()
    if "without" in args:
        found_category = ""
        found_types = [""]
        without = True
    else:    
        found_category, found_type = atp.classify_category(question)
        if found_category == "resource":
            found_types = atp.classify_resource(question)[0:10]
        else:
            found_types = [found_type]
        without = False
    
    t2 = time.time()
    extended_entities = ae.extend_entities(entities,found_category,found_types[0],without)
    t3 = time.time()
    answers = ae.answer_extractive(question,extended_entities)
    t4 = time.time()

    if "time" in args:
        response = {
            "category":found_category,
            "types":found_types[0],
            "answers":answers
            "times":[round(t2-t1),round(t3-t2),round(t4-t3),round(t4-t1)]
        }
    else:
        response = {
            "category":found_category,
            "types":found_types[0],
            "answers":answers
        }

    return jsonify(response)
   