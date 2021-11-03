import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
from confirmation_question import ConfirmationQuestion
from entity_expansion import get_entities_from_elas4rdf
import json
import time

app = flask.Flask(__name__)
# Initialize answer extraction and answer type prediction components
print('Initializing...')
ae = AnswerExtraction()
atp = AnswerTypePrediction()
cq = ConfirmationQuestion()
measure_time = True
# awnser type prediction
atp_ = True
# enrichment
enrich_ = True
print('\tDONE')


@app.route('/answer', methods=['GET'])
def api_answer():
    """
    Parameters: question - a natural language question
    Returns: question category, answer type, and a list of answers
    """
    args = request.args.to_dict()
    if 'question' in args:
        question = args['question']
    else:
        error_output = {'error': True}
        return jsonify(error_output)

    entities = get_entities_from_elas4rdf(question)
    """
    to improve performance when we receive a large number of entities
    we use only the first 10
    """
    number_of_entities = 10
    if len(entities) > number_of_entities:
        entities = entities[0:number_of_entities]

    if measure_time:
        start_atp = time.time()
    # enabled , disabled atp
    if atp_:
        found_category, found_type = atp.classify_category(question)
    else:
        found_category, found_type = '', ''

    max_types = 10
    if found_category == "resource":
        found_types = atp.classify_resource(question)[0:max_types]
    else:
        found_types = [found_type]
    # print(found_types)
    if measure_time:
        end_atp = time.time()
    atp_time = end_atp - start_atp

    if measure_time:
        start_extended_entities = time.time()
    extended_entities = ae.extend_entities(
        entities, found_category, found_types[0], enrich_)
    if measure_time:
        end_extended_entities = time.time()
    extended_entities_time = end_extended_entities - start_extended_entities

    if measure_time:
        start_answer_extraction = time.time()
    answers = ae.answer_extractive(
        question, extended_entities, found_category, cq)
    if measure_time:
        end_answer_extraction = time.time()
    answer_extraction_time = end_answer_extraction - start_answer_extraction

    if not measure_time:
        response = {
            "category": found_category,
            "types": found_types[0],
            "answers": answers,
        }
    else:
        response = {
            "category": found_category,
            "types": found_types[0],
            "answers": answers,
            "times":
            {
                "answer_type_prediction": atp_time,
                "extended_entities": extended_entities_time,
                "answer_extraction": answer_extraction_time,
                "total": atp_time+extended_entities_time+answer_extraction_time
            }
        }

    return jsonify(response)


@app.route('/', methods=['GET'])
def greet():
    return "Usage: /answer?question=..."
