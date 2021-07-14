'''
EXPERIMENT 2
this script reads qrels from qald2 (DBpedia-entity),system_output_entity.json and evaluates the queries answered by the QA
by the entity
'''

import json
import sys

system_output_path = "/home/nicolaig/elas4rdf_qa/evaluation/Experiment_2_3/entity_output.json"
qrels_path = "/home/nicolaig/elas4rdf_qa/evaluation/Experiment_2_3/qrels.txt"
threshold = float(sys.argv[1])


def getQrels():
    '''
    reads from qrels.txt and stores it as a dictionary
    '''
    qrels = {}
    with open(qrels_path, encoding="utf8") as qrel_file:
        for line in qrel_file:
            tokens = line.replace('\n', '').split('\t')
            q_id = tokens[0]
            entity = tokens[2][9:].replace('>', '')
            relevance = int(tokens[3])
            if q_id not in qrels:
                qrels[q_id] = {}
            qrels[q_id][entity] = relevance
    return qrels


def getrelevant(qrel):
    '''
    returns the relevant entities for the given query_id in qrel
    '''
    rel = {}
    for e in qrel:
        if qrel[e] > 0:
            rel[e] = qrel[e]
    return rel


def precisionAt_k(answers, relevant, k):
    rel_in_answer = 0
    if len(answers) == 0:
        return None
    # when the answer length < k , then the perfect score is less than 1
    length = len(answers) if len(answers) < k else k
    for i in range(0, length):
        entity = answers[i]['entity'].replace(
            'http://dbpedia.org/resource/', '')
        if entity in relevant:
            rel_in_answer += 1
    return rel_in_answer/k


def remove_answers(answers):
    a = []
    for i in range(len(answers)):
        if float(answers[i]['score']) >= threshold:
            a.append(answers[i])
    return a

### MAIN ###


qrels = getQrels()

with open(system_output_path, encoding="utf8") as jsonfile:
    system = json.load(jsonfile)
    scores = {"p1": [], "p3": [], "p5": []}
    for answer in system:
        relevant = getrelevant(qrels[answer['id']])
        answers = remove_answers(answer['entities'])
        # P@1 , P@3 , P@5 (Precision scores)
        p_1 = precisionAt_k(answers, relevant, 1)
        p_3 = precisionAt_k(answers, relevant, 3)
        p_5 = precisionAt_k(answers, relevant, 5)
        if p_1 != None:
            scores["p1"].append(p_1)
        if p_3 != None:
            scores["p3"].append(p_3)
        if p_5 != None:
            scores["p5"].append(p_5)

    p1 = sum(scores["p1"])/len(scores["p1"])
    p3 = sum(scores["p3"])/len(scores["p3"])
    p5 = sum(scores["p5"])/len(scores["p5"])
    print(p1*100.0, p3*100.0, p5*100.0)
