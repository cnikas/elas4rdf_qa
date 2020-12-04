from transformers import RobertaTokenizer, RobertaForQuestionAnswering, QuestionAnsweringPipeline
import torch
import answer_retrieval as ar

class AnswerExtraction:

    def __init__(self):
        model_name = "deepset/roberta-base-squad2"
        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaForQuestionAnswering.from_pretrained(model_name)
        self.pipeline = QuestionAnsweringPipeline(model=model,tokenizer=tokenizer,framework="pt",device=-1)
        
    def answer_extractive(self,question,entities):
        answers = []
        for e in entities:
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
        extended = []
        for e in entities:
            if(category=='literal'):
                sentences = ar.literal_sentences(e['uri'],atype)
            elif(category=='resource'):
                type_uri = 'http://dbpedia.org/ontology/'+atype
                sentences = ar.resource_sentences(e['uri'],type_uri)
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
