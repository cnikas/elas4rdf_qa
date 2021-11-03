"""
This script evaluates the system by comparing the system output with the ground
truth. It computes precision, recall, accuracy and F1 scores.
It is a modified version of the official evaluation script for SQuAD 2 
(https://rajpurkar.github.io/SQuAD-explorer/).
Example Usage:
`python evaluate.py system_output_filtered.json`
"""
import re
import collections
import json
import string
import sys

system_output_path = sys.argv[1]
failed = []
total_time = 0


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()
    normalized = []
    for ans in s:
        normalized.append(white_space_fix(
            remove_articles(remove_punc(lower(ans)))))
    return normalized


def compute_scores(a_gold, a_pred, output):
    question = output["question"]
    gold_toks = normalize_answer(a_gold)
    pred_toks = normalize_answer(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())

    text = ""

    for a in output["answers"]:
        text += a["text"] + " "

    text = normalize_answer(text.split())
    common_gold_in_text = sum((collections.Counter(
        text) & collections.Counter(gold_toks)).values())

    ideal_accuracy = {True: 1, False: 0}[common_gold_in_text > 0]

    if num_same == 0:
        failed.append({
            'question': question,
            'answer': a_pred,
            'gold': a_gold,
            "gold_tokens_in_text": common_gold_in_text
        })
        return [0, 0, 0, 0, ideal_accuracy]
    if num_same > 0:
        accuracy = 1
    else:
        accuracy = 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = f1Score(precision, recall)
    return [precision, recall, f1, accuracy, ideal_accuracy]


def f1Score(p, r):
    return (2*p*r)/(p+r)


def make_eval_dict(scores):
    total = len(scores)
    precision_scores = [i[0] for i in scores]
    p = sum(precision_scores) / total
    recall_scores = [i[1] for i in scores]
    r = sum(recall_scores) / total
    f1_scores = [i[2] for i in scores]
    f1 = f1Score(p, r)
    micro_f1 = sum(f1_scores) / total
    acc_scores = [i[3] for i in scores]
    ideal_acc = [i[4] for i in scores]
    avg_time = total_time / total
    return collections.OrderedDict([
        ('precision', 100.0 * p),
        ('recall', 100.0 * r),
        ('f1', 100.0 * f1),
        ('micro_f1', 100.0*micro_f1),
        ('accuracy', 100.0 * sum(acc_scores) / total),
        ('ideal_accuracy', 100.0*sum(ideal_acc)/total),
        ('total', total),
        ('failed', len(failed)*100.0/total),
        ('query average time', avg_time)
    ])


def main():
    with open(system_output_path, encoding="utf8") as jsonfile:
        system_output = json.load(jsonfile)
    with open("webquestions_test_converted.json", encoding="utf8") as jsonfile:
        ground_truth = json.load(jsonfile)
    scores = []
    total_counter = 0
    global total_time
    for q_output in system_output:
        if len(q_output["answers"]) > 0:
            total_counter += 1
            if "time" in q_output:
                total_time += float(q_output['time'])
            answers_output = [a["answer"] for a in q_output["answers"]]
            a_pred = []
            for a in answers_output:
                a_clean = a.split(" ")
                for ac in a_clean:
                    a_pred.append(ac)
            dict_gold = next(
                (q for q in ground_truth if q["id"] == q_output["id"]), None)
            if(dict_gold != None):
                gold_output = dict_gold["answers"]
                a_gold = []
                for a in gold_output:
                    a_clean = a.split(" ")
                    for ac in a_clean:
                        a_gold.append(ac)
                scores.append(compute_scores(
                    a_gold, a_pred, q_output))
    out_eval = make_eval_dict(scores)
    with open("failed_questions.json", "w", encoding="utf8") as fail:
        fail.write(json.dumps(failed))
    print(json.dumps(out_eval, indent=2))
    print("Failed: "+str(len(failed)))
    print("Average Query Time: "+str(total_time/total_counter))


if __name__ == '__main__':
    main()