import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
import answer_retrieval as ar
import json
import re

app = flask.Flask(__name__)
app.config['SECRET_KEY'] =  'e2b35432632f190f45201266'
#print('Initializing...')
#ae = AnswerExtraction()
#atp = AnswerTypePrediction()
#print('\tDONE')
 
@app.route('/answer', methods=['GET'])
def api_answer():
    args = request.args.to_dict()

    if 'question' in args:
        question = args['question']
    else:
        error_output = {'error':True}
        return jsonify(error_output)

    found_category, found_type = atp.classify_category(question)

    if found_category == "resource":
        found_types = atp.classify_resource(question)[0:10]
    else:
        found_types = [found_type]

    entities_json = json.loads(args['entities'])
    entities = [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in entities_json['results']['entities']]
    print(entities)
    extended_entities = ae.extend_entities(entities,found_category,found_types[0])
    answers = ae.answer_extractive(question,extended_entities)

    response = {
        "category":found_category,
        "types":found_types,
        "entities":extended_entities,
        "answers":answers
    }

    return jsonify(response)
   
if __name__ == "__main__":
    print('Initializing...')
    ae = AnswerExtraction()
    atp = AnswerTypePrediction()
    print('\tDONE')
    app.run(host= '0.0.0.0')