from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import json


class ConfirmationQuestion:
    # this class contains methods for the confirmation question or boolean question
    def __init__(self):
        # initialize pretrained model
        model_dir = './resources/confirmation_model'
        self.model = RobertaForSequenceClassification.from_pretrained(
            model_dir)
        self.tokenizer = RobertaTokenizer.from_pretrained(model_dir)
        self.device = torch.device(
            "cuda"if torch.cuda.is_available() else"cpu")

    def predict(self, question, passage):
        # given a question and a passage determine if the passage fulfills the question

        # use truncation form bigger inputs
        sequence = self.tokenizer.encode_plus(question, passage, return_tensors="pt", truncation=True)[
            'input_ids'].to(self.device)

        logits = self.model(sequence)[0]
        probabilities = torch.softmax(logits, dim=1).detach().cpu().tolist()[0]
        proba_yes = round(probabilities[1], 2)
        proba_no = round(probabilities[0], 2)

        return {
            'question': question,
            'answer': {True: 'yes', False: 'no'}[proba_yes > proba_no],
            'score': max(proba_yes,proba_no),
            'yes': proba_yes,
            'no': proba_no
        }
