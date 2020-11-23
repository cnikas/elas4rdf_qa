import answer_retrieval as rest
import csv
from transformers import RobertaTokenizer, RobertaForQuestionAnswering, QuestionAnsweringPipeline
import torch
import re
import json
from answer_type_prediction import AnswerTypePrediction

class AnswerExtraction:

    def __init__(self):
        model_name = "deepset/roberta-base-squad2"
        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaForQuestionAnswering.from_pretrained(model_name)
        self.pipeline = QuestionAnsweringPipeline(model=model,tokenizer=tokenizer,framework="pt",device=-1)
        self.atp = AnswerTypePrediction()
        self.stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    
    def extract_answer(self,question):
        found_category = self.atp.classify_category(question)
        found_types = self.atp.predict_answer_type(question,found_category)
        found_answers = self.answer_extractive(question)
        return [found_category, found_types, found_answers]

    def answer_extractive(self,question):
        q_no_stopwords = filtered_words = ' '.join([word for word in question.split() if word not in self.stopwords])
        entities = rest.get_entities(q_no_stopwords,10)
        answers = []
        for e in entities:
            output = self.pipeline(question,e['rdfs_comment'])
            answers.append({'entity':e['uri'],'answer':output['answer'],'score':output['score']})
        return sorted(answers, key=lambda k: k['score'],reverse=True) 

if __name__ == "__main__":
    ae = AnswerExtraction()
    ae.answer_from_entities("who is the father of Queen Elizabeth II?")