import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
import answer_retrieval as ar
import json

app = flask.Flask(__name__)
app.config['SECRET_KEY'] =  'e2b35432632f190f45201266'
stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
print('Initializing...')
ae = AnswerExtraction()
atp = AnswerTypePrediction()
print('\tDONE')



@app.route('/answer', methods=['GET'])
def api_answer():
    args = request.args.to_dict(flat=False)

    if 'question' in args:
        question = args['question'][0]
    else:
        error_output = {'error':True}
        return jsonify(error_output)

    found_category, found_type = atp.classify_category(question)

    if found_category == "resource":
        found_types = atp.classify_resource(question)[0:10]
    else:
        found_types = [found_category]

    q_no_stopwords = filtered_words = ' '.join([word for word in question.split() if word not in stopwords])
    entities = ar.get_entities(q_no_stopwords,10)
    
    answers = ae.answer_extractive(question,entities)

    response = {
        "category":found_category,
        "types":found_types,
        "entities":entities,
        "answers":answers
    }
    print(response)

    return jsonify(response)

@app.route('/update', methods=['GET'])
def api_update():
    args = request.args.to_dict(flat=False)

    required = ['question','category','type','selected_entities']
    if(not all(arg in args for arg in required)):
        error_output = {'error':True}
        return jsonify(error_output)

    question = args['question'][0]
    found_category = args['category'][0]
    
    selected_type = args['type'][0]
    
    selected_entities = args['selected_entities']
    entities = ar.get_entities_updated(selected_entities,selected_type)
    print(entities)
    answers = ae.answer_extractive(question,entities)
    
    response = {
        "category":found_category,
        "types":[selected_type],
        "entities":entities,
        "answers":answers
    }

    return jsonify(response)

@app.route('/more_entities', methods=['GET'])
def api_more_entities():
    args = request.args.to_dict(flat=False)

    required = ['type','entities']
    if(not all(arg in args for arg in required)):
        error_output = {'error':True}
        return jsonify(error_output)

    selected_type = args['type'][0]
    
    selected_entities = args['entities']
    entities = ar.get_entities_updated(selected_entities,selected_type)

    return jsonify(entities)
   
if __name__ == "__main__":
    print('Initializing...')
    ae = AnswerExtraction()
    atp = AnswerTypePrediction()
    print('\tDONE')
    app.run(host= '0.0.0.0')