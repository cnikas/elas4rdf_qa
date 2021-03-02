import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
from entity_expansion import get_entities_from_elas4rdf
import json

app = flask.Flask(__name__)
app.config['SECRET_KEY'] =  'e2b35432632f190f45201266'
# Initialize answer extraction and answer type prediction components
print('Initializing...')
ae = AnswerExtraction()
atp = AnswerTypePrediction()
print('\tDONE')

"""
Parameters: question - a natural language question
Returns: question category, answer type, and a list of answers
""" 
@app.route('/answer', methods=['GET'])
def api_answer():

    args = request.args.to_dict()
    if 'question' in args:
        question = args['question']
    else:
        error_output = {'error':True}
        return jsonify(error_output)

    entities = get_entities_from_elas4rdf(question)

    found_category, found_type = atp.classify_category(question)
    if found_category == "resource":
        found_types = atp.classify_resource(question)[0:10]
    else:
        found_types = [found_type]
    
    extended_entities = ae.extend_entities(entities,found_category,found_types[0])
    answers = ae.answer_extractive(question,extended_entities)
    
    response = {
        "category":found_category,
        "types":found_types[0],
        "answers":answers
    }

    return jsonify(response)

@app.route('/', methods=['GET'])
def greet():
    return "Usage: /answer?question=..."