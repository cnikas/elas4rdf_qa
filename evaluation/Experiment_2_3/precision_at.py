"""
Precision @ 
"""
import csv
import re
import collections
import json
import string

qrels = []
with open('qrels-v2.txt',encoding='utf8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        if int(row[3]) > 0: 
            qrels.append(row)
            
queries = []
with open('queries-v2_stopped.txt',encoding='utf8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for row in spamreader:
        queries.append(row)
        
def clean(s):
    s = s[s.index(':')+1:-1]
    s = s.replace('_',' ')
    s = s.lower()
    return s

dataset = []
for q in queries:
    if q[0].startswith("QALD"):
        id = q[0]
        question = q[1]
        answers = []
        for a in qrels:
            if a[0] == id:
                answers.append(clean(a[2]))
        dataset.append({
            "id" : id,
            "question" : question,
            "answers" : answers
        })
        
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
        normalized.append(white_space_fix(remove_articles(remove_punc(lower(ans)))))
    return normalized


def compute_scores(a_gold, a_pred):
    gold_toks = normalize_answer(a_gold)
    pred_toks = normalize_answer(a_pred)
    common = collections.Counter(gold_toks) \
        & collections.Counter(pred_toks)
    num_same = sum(common.values())

    if num_same == 0:
        return [0, 0, 0, 0]
    if num_same > 0:
        accuracy = 1
    else:
        accuracy = 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = 2 * precision * recall / (precision + recall)
    return [precision, recall, f1, accuracy]


def make_eval_dict(scores):
    total = len(scores)
    precision_scores = [i[0] for i in scores]
    recall_scores = [i[1] for i in scores]
    f1_scores = [i[2] for i in scores]
    acc_scores = [i[3] for i in scores]
    return collections.OrderedDict([('precision', 100.0
                                   * sum(precision_scores) / total),
                                   ('recall', 100.0
                                   * sum(recall_scores) / total), ('f1'
                                   , 100.0 * sum(f1_scores) / total),
                                   ('accuracy', 100.0 * sum(acc_scores)
                                   / total), ('total', total)])


def precisionat(n,t):
    with open('system_output.json', encoding='utf8') as jsonfile:
        system_output = json.load(jsonfile)
    ground_truth = dataset
    scores = []
    total_counter = 0
    system_output = ans_threshold(system_output,t)
    for q_output in system_output:
        if len(q_output['answers']) > 0:
            answers_output = [a['answer'] for a in q_output['answers']]
            a_pred = []
            for a in answers_output[0:n]:
                a_clean = a.split(' ')
                for ac in a_clean:
                    a_pred.append(ac)
            dict_gold = next((q for q in ground_truth if q['id']
                             == q_output['id']), None)
            if dict_gold != None:
                gold_output = dict_gold['answers']
                a_gold = []
                for a in gold_output:
                    a_clean = a.split(' ')
                    for ac in a_clean:
                        a_gold.append(ac)
                scores.append(compute_scores(a_gold, a_pred))
    out_eval = make_eval_dict(scores)
    return out_eval["precision"]

    
def ans_threshold(input,t):
    out = []
    for q in input:
        newans = []
        for ans in q['answers']:
            if float(ans['score']) >= t: 
                newans.append(ans)
        out.append({
            "id": q["id"],
            "question": q["query"],
            "answers": newans
        })
    return out

for t in range(0,10,1):
    threshold = t/10
    print("t: %f, p@1: %.3f, p@3: %.3f, p@5: %.3f" % (threshold, precisionat(1,threshold), precisionat(3,threshold), precisionat(5,threshold)))