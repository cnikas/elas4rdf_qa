from functools import total_ordering
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import json
import time


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
            'score': max(proba_yes, proba_no),
            'yes': proba_yes,
            'no': proba_no
        }


def load_dataset():
    dataset = []
    with open('./boolq/train.jsonl', 'r', encoding='utf-8') as data:
        lines = data.readlines()
        for line in lines:
            dataset.append(json.loads(line))
    return dataset


cq = ConfirmationQuestion()
# q = "does damon and elena get together in season 3"
# p = "In the third season, Damon helps Elena in bringing his brother, Stefan, back to Mystic Falls after Stefan becomes Klaus' henchman. The arrangement transpired after a bargain for his blood that would cure Damon of the werewolf bite he had received from Tyler. At first, he is reluctant to involve Elena in the rescue attempts, employing Alaric Saltzman, Elena's guardian, instead as Klaus does not know that Elena is alive after the sacrifice which frees Klaus' hybrid side. However, Elena involves herself, desperate to find Stefan. Damon, though hesitant at first, is unable to refuse her because of his love for her. He also points out to her that she once turned back from finding Stefan since she knew Damon would be in danger, clearly showing that she also has feelings for him. He tells her that ``when (he) drag(s) (his) brother from the edge to deliver him back to (her), (he) wants her to remember the things (she) felt while he was gone.'' When Stefan finally returns to Mystic Falls, his attitude is different from that of the first and second seasons. This causes a rift between Elena and Stefan whereas the relationship between Damon and Elena becomes closer and more intimate. A still loyal Elena, however, refuses to admit her feelings for Damon. In 'Dangerous Liaisons', Elena, frustrated with her feelings for him, tells Damon that his love for her may be a problem, and that this could be causing all their troubles. This incenses Damon, causing him to revert to the uncaring and reckless Damon seen in the previous seasons. The rocky relationship between the two continues until the sexual tension hits the fan and in a moment of heated passion, Elena -- for the first time in the three seasons -- kisses Damon of her own accord. This kiss finally causes Elena to admit that she loves both brothers and realize that she must ultimately make her choice as her own ancestress, Katherine Pierce, who turned the brothers, once did. In assessment of her feelings for Damon, she states this: ``Damon just sort of snuck up on me. He got under my skin and no matter what I do, I can't shake him.'' In the season finale, a trip designed to get her to safety forces Elena to make her choice: to go to Damon and possibly see him one last time; or to go to Stefan and her friends and see them one last time. She chooses the latter when she calls Damon to tell him her decision. Damon, who is trying to stop Alaric, accepts what she says and she tells him that maybe if she had met Damon before she had met Stefan, her choice may have been different. This statement causes Damon to remember the first night he did meet Elena which was, in fact, the night her parents died - before she had met Stefan. Not wanting anyone to know he was in town and after giving her some advice about life and love, Damon compels her to forget. He remembers this as he fights Alaric and seems accepting of his death when Alaric, whose life line is tied to Elena's, suddenly collapses in his arms. Damon is grief-stricken, knowing that this means that Elena has also died and yells, ``No! You are not dead!'' A heartbroken Damon then goes to the hospital demanding to see Elena when the doctor, Meredith Fell, tells him that she gave Elena vampire blood. The last shot of the season finale episode shows Elena in transition."

# res = cq.predict(q, p)

# print(res)


dataset = load_dataset()

total = len(dataset)
total_time = 0
correct = 0
i = 0
for q in dataset:
    i += 1
    question = str(q['question'])
    passage = str(q['passage'])
    start = time.time()
    res = cq.predict(question, passage)
    end = time.time()
    total_time += (end - start)
    ans = None
    if res['yes'] > res['no']:
        ans = True
    else:
        ans = False
    if q['answer'] == ans:
        correct += 1
    print(str(i)+"/"+str(total))
    print(total_time/i)

print({
    "Accuracy": correct/total,
    "Average Query Time": total_time/total
})
