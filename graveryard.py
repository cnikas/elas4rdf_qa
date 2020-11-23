#import numpy as np
#from numpy import dot
#from numpy.linalg import norm
#import gensim
#import gensim.downloader as api    
    def __init__(self):
        #model = api.load('glove-wiki-gigaword-100')
        #self.model = model
        #self.stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        #hierarchy_json = resources_dir+'/dbpedia_hierarchy.json'
        #hierarchy = {}
        #with open(hierarchy_json) as json_file:
        #    hierarchy = json.load(json_file)
        #self.hierarchy = hierarchy
        #self.pipeline = QuestionAnsweringPipeline(model=self.model,tokenizer=self.tokenizer,framework="pt")

    def extract_answers(self,question,category,types,entities):
        answers = []
        accepted_types = []
        if(category == 'boolean'):
            answers.append(self.answer_boolean())
        elif(category == 'literal'):
            if(types[0] == 'date'):
                accepted_types = ['http://www.w3.org/2001/XMLSchema#date']
            elif(types[0] == 'number'):
                accepted_types = ['http://www.w3.org/2001/XMLSchema#integer','http://www.w3.org/2001/XMLSchema#float','http://www.w3.org/2001/XMLSchema#double']
            else:
                accepted_types = ['http://www.w3.org/2001/XMLSchema#string']

            for e in entities:
                answers.extend(rest.objects_in_range(e['uri']))
        else:
            accepted_types = types[0:5]
            answers.extend(self.get_entity_answers(entities))
            for e in entities:
                answers.extend(rest.objects_of_type(e['uri']))
        
        q_vector = self.compute_sequence_vector(question)

        answers = self.compute_similarities(q_vector,answers)
        answers = self.filter_answers(answers,accepted_types,0.5,0.7)
        answers = sorted(answers, key=lambda k: k['similarity'], reverse=True)
        return answers[0:10]

    def compute_sequence_vector(self,q):
        vocab = self.model.vocab.keys()
        try:
            sentence = re.sub(r'[^A-Za-z0-9 ]+', '', q).lower().split(' ')
        except TypeError:
            print(q)
        vectors=[]
        for w in sentence:
            if (w in vocab) and (w not in self.stopwords):
                vectors.append(self.model[w])
        if(vectors==[]):
            return np.zeros(100,dtype='float32')
        else:
            return np.average(vectors,axis=0)

    def compute_similarities(self,q_vector,answers):
        if q_vector.any():
            for a in answers:
                if(a['answerType'] != 'boolean'):
                    a_vector = self.compute_sequence_vector(a['predicateLabel'])
                    a['similarity'] = self.compute_similarity(q_vector,a_vector)
                else:
                    a['similarity'] = 0
        else:
            for a in answers:
                a['similarity'] = 0
        return answers

    def compute_similarity(self,v_a,v_b):
        if(v_a.any() and v_b.any()):
            return (dot(v_a, v_b)/(norm(v_a)*norm(v_b))).item()
        else:
            return 0
            
    def answer_boolean(self):
        return {'answerType':'boolean'}

    def filter_answers(self,answers,accepted_types,low_t,high_t):
        ats = set(accepted_types)
        for at in accepted_types:
            if at in self.hierarchy:
                ats.update(set(self.hierarchy[at]['children']))
        accepted_types_with_children = ['http://dbpedia.org/ontology/'+t[4:] for t in ats]
        filtered = []
        for a in answers:
            if (a['answerType'] in accepted_types_with_children and a['similarity'] > low_t) or (a['similarity'] > high_t):
                filtered.append(a)
            
        return filtered

    def get_entity_answers(self,entities):
        answers = []
        for e in entities:
            sentence = re.sub(r"\[ *| *@en\]",'',e['rdfs_comment'])
            answers.append({
                    'answer' : e['uri'],
                    'predicateLabel' : sentence,
                    'answerType' : 'entity'
                })
        return answers


        @app.route('/answer', methods=['GET'])
def api_answer():
    args = request.args.to_dict(flat=False)
    
    if 'question' in args:
        question = args['question'][0]
    else:
        return 'no question given'

    if 'category' in args:
        category = args['category'][0]
    else:
        category, basic_type = atp.classify_category(args['question'][0])

    if 'types' in args:
        types = args['types']
    else:
        types = atp.predict_answer_type(question,category)

    if 'entities' in args:
        entities = args['entities']
    else:
        entities = rest.get_entities(question,10)

    answers = ae.extract_answers(question,category,types,entities)

    response = {
        'question':question,
        'category':category,
        'types':types,
        'entities':entities,
        'answers':answers
    }

    return jsonify(response)

    
@app.route('/entities', methods=['GET'])
def api_entities():
    args = request.args.to_dict()
    
    if 'question' in args:
        question = args['question'][0]
        entities = rest.get_entities(question,10)
    else:
        return 'no question given'

    return jsonify(entities)

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import numpy as np
import csv
import json

class AnswerTypePrediction:
    def __init__(self,resources_dir):
        category_model_dir = './resources/category_model'
        resource_model_dir = './resources/resource_model'
        mapping_csv = resources_dir+'./resources/mapping.csv'
        hierarchy_json = resources_dir+'./resources/dbpedia_hierarchy.json'
        id_to_label = {}
        label_to_id = {}
        with open(mapping_csv) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                id_to_label[row[0]] = row[1]
                label_to_id[row[1]] = row[0]
        self.id_to_label = id_to_label
        self.label_to_id = label_to_id
        self.category_tokenizer = DistilBertTokenizer.from_pretrained(category_model_dir)
        self.category_model = DistilBertForSequenceClassification.from_pretrained(category_model_dir,num_labels=5)
        self.resource_tokenizer = BertTokenizer.from_pretrained(resource_model_dir)
        self.resource_model = BertForSequenceClassification.from_pretrained(resource_model_dir,num_labels=len(id_to_label))
        hierarchy = {}
        with open(hierarchy_json) as json_file:
            hierarchy = json.load(json_file)
        self.hierarchy = hierarchy

    def classify_category(self,q):
        input_ids = torch.tensor(category_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)
        with torch.no_grad():
            outputs = category_model(input_ids)
        logits = outputs[0]
        result = np.argmax(logits.detach().numpy(),axis=1)[0]
        categories = ['boolean','literal','literal','literal','resource']
        types = ['boolean','date','number','string','']
        return categories[result], types[result]

    def classify_resource(self,q):
        input_ids = torch.tensor(self.resource_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)  # Batch size 1
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        with torch.no_grad():
            outputs = self.resource_model(input_ids, labels=labels)
        logits = outputs[1]
        l_array = logits.detach().numpy()[0]
        #normalize logits so that max is 1
        norm = [float(i)/max(l_array) for i in l_array]
        result_before = np.argsort(norm)[::-1]
        #reward top class
        initial_top_index = np.argmax(norm)
        initial_top = self.hierarchy[self.id_to_label[str(initial_top_index)]]
        if initial_top != {}:
            norm[initial_top_index] = norm[initial_top_index] + int(initial_top['level'])/6
            #reward sub classes of top class
            initial_top_children = initial_top['children']
            for c in initial_top_children:
                if c in self.label_to_id:
                    norm[int(self.label_to_id[c])] = norm[int(self.label_to_id[c])] + int(self.hierarchy[c]['level'])/6
        #classes in descending order
        result = np.argsort(norm)[::-1]
        result_mapped = []
        for r in result:
            result_mapped.append(self.id_to_label[str(r)])
        return result_mapped
    
    def predict_answer_type(self,q,found_category,found_type):
        if found_category == 'resource':
            found_type = self.classify_resource(q)[0:10]
        else:
            found_type = [found_type]
        return found_type
