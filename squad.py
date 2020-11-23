from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad",return_dict=True)

pipeline = QuestionAnsweringPipeline(model=model,tokenizer=tokenizer,framework="pt")
pipeline(question=question,context=text)

def answer_from_entities(self,question,entities):
	answers = []
	for e in entities:
		output = pipeline(question=question,text=e['rdfs_comment'])
		answers.append({'entity':e['uri'],'output':output})
	newlist = sorted(answers, key=lambda k: k['output']['score'])
	print(newlist) 

def use_model(question,text):
	inputs = tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs)

    answer_start = torch.argmax(answer_start_scores)  
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    
    return answer