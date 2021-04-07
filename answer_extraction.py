# from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, QuestionAnsweringPipeline
from transformers import RobertaForQuestionAnswering, RobertaTokenizer, QuestionAnsweringPipeline
import torch
import entity_expansion as expansion

class AnswerExtraction:
    # This class contains methods for the answer extraction stage

    def __init__(self):
        # Initalisation of pretrained extractive QA model
        model_name = "deepset/roberta-base-squad2"
        #model_name = "distilbert-base-uncased-distilled-squad" 
        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaForQuestionAnswering.from_pretrained(model_name)
        self.pipeline = QuestionAnsweringPipeline(model=model,tokenizer=tokenizer,framework="pt",device=-1)

    def answer_extractive(self,question,entities):
        # Obtain a question from each given entity
        answers = []
        for e in entities:
            print('ans'+e['uri'])
            if e['text'] != '':
                output = self.pipeline(question,e['text'])
                highlighted_text = e['text'][0:output['start']]+'<b>'+e['text'][output['start']:output['end']]+'</b>'+e['text'][output['end']:] 
                answers.append({
                    'entity':e['uri'],
                    'answer':output['answer'],
                    'score':round(output['score'],3),
                    'text':highlighted_text
                    })
        return sorted(answers, key=lambda k: k['score'],reverse=True) 

    def extend_entities(self,entities,category,atype):
        # Extend entity descriptions with RDF nodes matching the answer type
        extended = []
        for e in entities:
            print('ext'+e['uri'])
            if(category=='literal'):
                sentences = expansion.literal_sentences(e['uri'],atype)
            elif(category=='resource'):
                type_uri = 'http://dbpedia.org/ontology/'+atype
                sentences = expansion.resource_sentences(e['uri'],type_uri)
            else:
                sentences = []
            if(e['rdfs_comment'] == "[]"):
                clean_rdfs_comment = ""
            else:
                clean_rdfs_comment = e['rdfs_comment'][3:-4]
            new_text = clean_rdfs_comment + ". ".join(sentences)
            extended.append({
                'uri':e['uri'],
                'text':new_text
                })
        return extended
