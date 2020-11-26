import flask
from flask import request, jsonify
from answer_extraction import AnswerExtraction
from answer_type_prediction import AnswerTypePrediction
import answer_retrieval as ar
import json
import re

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
    entities = ar.get_entities(re.sub('[^a-zA-Z0-9 ]', '', q_no_stopwords),10)
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