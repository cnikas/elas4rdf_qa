# from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, QuestionAnsweringPipeline
import collections
from re import S
from transformers import RobertaForQuestionAnswering, RobertaTokenizer, QuestionAnsweringPipeline
import torch
import entity_expansion as expansion


class AnswerExtraction:
    # This class contains methods for the answer extraction stage

    def __init__(self):
        self.device = torch.device(
            "cuda"if torch.cuda.is_available() else"cpu")
        # Initalisation of pretrained extractive QA model
        model_name = "deepset/roberta-base-squad2"
        # model_name = "distilbert-base-uncased-distilled-squad"
        tokenizer = RobertaTokenizer.from_pretrained(model_name)
        model = RobertaForQuestionAnswering.from_pretrained(model_name)
        self.pipeline = QuestionAnsweringPipeline(
            model=model, tokenizer=tokenizer, framework="pt", device=-1)

    def combineAnswers(self, answers):
        '''
        combine same answers and sum scores
        '''
        combined = []

        for i in answers:
            for j in answers:
                if i['answer'] == j['answer'] and i != j:
                    # combine answer
                    answer = i['answer']
                    # combine entities
                    entities = []
                    entities.append(i['entity'])
                    entities.append(j['entity'])
                    # combine score
                    score = i['score'] + j['score']
                    if score > 1.0:
                        score = 1.0
                    # combine texts
                    texts = []
                    texts.append(i['text'])
                    texts.append(j['text'])
                    combined.append({
                        'answer': answer,
                        'entities': entities,
                        'score': score,
                        'texts': texts
                    })
                    answers.remove(i)
                    answers.remove(j)

        for i in answers:
            combined.append(i)

        return combined

    def score_boolean(self, answers, question):
        '''
        score boolean answers
        50% common tokens entity - question
        50% yes/no score
        '''
        question_tokens = question.lower().split(" ")
        new_answers = []
        for a in answers:
            entity_tokens = expansion.entity_to_str(
                a['entity']).lower().split(" ")
            common = collections.Counter(
                question_tokens) & collections.Counter(entity_tokens)
            same = sum(common.values())
            common_score = same / len(entity_tokens)
            # print("------")
            # print(entity_tokens)
            # print(question_tokens)
            # print(same)
            # print("------")
            a['score'] = round((a['score'] + common_score) / 2, 3)
            new_answers.append(a)
        return new_answers

    def answer_extractive(self, question, entities, category, confirmationQuestion=None):
        # Obtain a question from each given entity
        answers = []
        for e in entities:
            # print('ans'+e['uri'])
            if e['text'] != '':
                # handle answer depending on category
                if category == 'boolean':
                    output = confirmationQuestion.predict(question, e['text'])
                    highlighted_text = e['text']
                else:
                    output = self.pipeline(question, e['text'])
                    highlighted_text = e['text'][0:output['start']]+'<b>' + \
                        e['text'][output['start']:output['end']] + \
                        '</b>'+e['text'][output['end']:]
                answers.append({
                    'entity': e['uri'],
                    'answer': output['answer'],
                    'score': round(output['score'], 3),
                    'text': highlighted_text
                })
        if category == 'boolean':
            answers = self.score_boolean(answers, question)
        #answers = self.combineAnswers(answers)
        return sorted(answers, key=lambda k: k['score'], reverse=True)

    def extend_entities(self, entities, category, atype, enrich=True):
        # Extend entity descriptions with RDF nodes matching the answer type
        extended = []
        for e in entities:
            # print('ext'+e['uri'])
            if(category == 'literal' and enrich == True):
                sentences = expansion.literal_sentences(e['uri'], atype)
            elif(category == 'resource' and enrich == True):
                type_uri = 'http://dbpedia.org/ontology/'+atype
                sentences = expansion.resource_sentences(e['uri'], type_uri)
            # boolean type or no type enrichment
            elif(
                ((category == '' and atype == '') or (category == 'boolean'))
                    and enrich == True):
                # enrichment without type
                sentences = expansion.extend_ignore_type(e['uri'])
            else:  # no enrichment
                sentences = []
            if(e['rdfs_comment'] == "[]"):
                clean_rdfs_comment = ""
            else:
                clean_rdfs_comment = e['rdfs_comment'][3:-4]
            new_text = clean_rdfs_comment + ". ".join(sentences)
            # print(e['rdfs_comment'])
            extended.append({
                'uri': e['uri'],
                'text': new_text
            })
        return extended
