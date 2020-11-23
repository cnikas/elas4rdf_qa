import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
import answer_retrieval as rest
import json

app = flask.Flask(__name__)
app.config['SECRET_KEY'] =  'e2b35432632f190f45201266'

@app.route('/answer', methods=['GET'])
def api_answer():
    args = request.args.to_dict(flat=False)

    if 'question' in args:
        question = args['question'][0]
    else:
        return 'no question given'
    
    output = ae.extract_answer(question)
    return jsonify(output)

if __name__ == "__main__":
    print('Initializing...')
    ae = AnswerExtraction()
    print('\tDONE')
    app.run()