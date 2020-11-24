from transformers import RobertaTokenizer, RobertaForQuestionAnswering, QuestionAnsweringPipeline
import torch

class AnswerExtraction:

    def __init__(self):
        model_name = "deepset/roberta-base-squad2"
        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaForQuestionAnswering.from_pretrained(model_name)
        self.pipeline = QuestionAnsweringPipeline(model=model,tokenizer=tokenizer,framework="pt",device=-1)
        
    def answer_extractive(self,question,entities):
        answers = []
        for e in entities:
            output = self.pipeline(question,e['rdfs_comment'])
            answers.append({'entity':e['uri'],'answer':output['answer'],'score':output['score']})
        return sorted(answers, key=lambda k: k['score'],reverse=True) 