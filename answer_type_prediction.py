from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import numpy as np
import csv
import json

class AnswerTypePrediction:
    def __init__(self):
        category_model_dir = './resources/category_model'
        resource_model_dir = './resources/resource_type_model'
        mapping_csv = './resources/mapping.csv'
        hierarchy_json = './resources/dbpedia_hierarchy.json'
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
        self.resource_tokenizer = DistilBertTokenizer.from_pretrained(resource_model_dir)
        self.resource_model = DistilBertForSequenceClassification.from_pretrained(resource_model_dir,num_labels=len(id_to_label))
        hierarchy = {}
        with open(hierarchy_json) as json_file:
            hierarchy = json.load(json_file)
        self.hierarchy = hierarchy

    def classify_category(self,q):
        input_ids = torch.tensor(self.category_tokenizer.encode(q, add_special_tokens=True)).unsqueeze(0)
        with torch.no_grad():
            outputs = self.category_model(input_ids)
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
        return list(map(lambda x: x[x.rindex(':')+1:],result_mapped))
    
    def predict_answer_type(self,q,found_category):
        if found_category == 'resource':
            found_type = self.classify_resource(q)[0:10]
        else:
            found_type = [found_category]
        return found_type
