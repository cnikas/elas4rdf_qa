'''
EXPERIMENT 3
'''

import requests
import json
import math
from operator import itemgetter
from copy import deepcopy

system_output_path = "/home/nicolaig/elas4rdf_qa/evaluation/Experiment_2_3/system_output.json"
qrels_path = "/home/nicolaig/elas4rdf_qa/evaluation/Experiment_2_3/qrels.txt"
output_file = "system_output_qa_ranking.json"


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


def mergeQaEntities(entities, qa_answers):
    '''
    Keep the score from each entity and answer as computed by the entity search
    system and question answering component.
    '''
    res = deepcopy(entities + qa_answers)
    for e in res:
        e['score'] = float(e['score'])
    return sorted(res, key=lambda i: i['score'], reverse=True)


def mergeQaEntitiesAndScores(entities, qa_answers):
    '''
    Sum scores for entities in both rankings
    '''

    res1 = deepcopy(entities)
    # sum scores
    for e in res1:
        e['score'] = float(e['score'])
        for a in qa_answers:
            if e['entity'] == a['entity']:
                e['score'] += a['score']
    res2 = deepcopy(qa_answers)
    for e in res2:
        for a in entities:
            a['score'] = float(a['score'])
            if e['entity'] == a['entity']:
                e['score'] += a['score']
    res = res1 + res2
    return sorted(res, key=lambda i: i['score'], reverse=True)


def convertAnswer(answer, qrels):
    res = []
    for a in answer:
        entity = a['entity'].replace('http://dbpedia.org/resource/', '')
        if entity in qrels:
            res.append({"entity": entity, "relevance": qrels[entity]})

    return res  # sorted(res, key=lambda x: x["relevance"], reverse=True)


def DCG(answer, qrels, at):
    # scale: 2 =  very relevant , 1 = relevant , 0  = irrelevant
    dcg = 0
    i = 1
    for e in answer:
        if e["entity"] in qrels:
            dcg += (2**(e["relevance"])-1)/(math.log2(i+1))
            i += 1
        if i > at:
            break
    return dcg


def NDCG(answer, qrels, q_id, at):

    converted_a = convertAnswer(answer, qrels[q_id])
    relevant = []
    for e in qrels[q_id]:
        relevant.append({"entity": e, "relevance": qrels[q_id][e]})
    relevant = sorted(relevant, key=lambda x: x["relevance"], reverse=True)

    dcg = DCG(converted_a, qrels[q_id], at)
    ideal_dcg = DCG(relevant, qrels[q_id], at)
    if ideal_dcg != 0:
        return dcg/ideal_dcg
    else:
        return 0


def get_entities(query, size=1000):
    url = "https://demos.isl.ics.forth.gr/elas4rdf/entities_json"
    payload = {
        "query": query,
        "size": str(size)
    }
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=payload, headers=headers)
    response_json = response.json()
    entities = response_json['results']['entities']
    return entities


qrels = getQrels()

with open(system_output_path, encoding="utf8") as jsonfile:
    system = json.load(jsonfile)
    scores = {
        # 0 ,1 ,3 etc represents answers added from QA
        'approach1': {
            0: {"ndcg10": [], "ndcg100": []}, 1: {"ndcg10": [], "ndcg100": []},
            3: {"ndcg10": [], "ndcg100": []}, 5: {"ndcg10": [], "ndcg100": []}, 10: {"ndcg10": [], "ndcg100": []}
        },
        'approach2': {
            0: {"ndcg10": [], "ndcg100": []}, 1: {"ndcg10": [], "ndcg100": []},
            3: {"ndcg10": [], "ndcg100": []}, 5: {"ndcg10": [], "ndcg100": []}, 10: {"ndcg10": [], "ndcg100": []}
        }
    }
    i = 1
    for answer in system:
        print(answer['query']+'\t'+str(i)+' of 140')
        i += 1
        entities = get_entities(answer['query'])
        # an_ek , n = approach , k = answers added from QA
        a1_e0 = mergeQaEntities(entities, [])
        a1_e1 = mergeQaEntities(entities, answer["answers"][:1])
        a1_e3 = mergeQaEntities(entities, answer["answers"][:3])
        a1_e5 = mergeQaEntities(entities, answer["answers"][:5])
        a1_e10 = mergeQaEntities(entities, answer["answers"][:10])

        a2_e0 = mergeQaEntities(entities, [])
        a2_e1 = mergeQaEntitiesAndScores(entities, answer["answers"][:1])
        a2_e3 = mergeQaEntitiesAndScores(entities, answer["answers"][:3])
        a2_e5 = mergeQaEntitiesAndScores(entities, answer["answers"][:5])
        a2_e10 = mergeQaEntitiesAndScores(entities, answer["answers"][:10])

        # aproach 1
        scores['approach1'][0]['ndcg10'].append(
            NDCG(a1_e0, qrels, answer['id'], 10))
        scores['approach1'][0]['ndcg100'].append(
            NDCG(a1_e0, qrels, answer['id'], 100))
        scores['approach1'][1]['ndcg10'].append(
            NDCG(a1_e1, qrels, answer['id'], 10))
        scores['approach1'][1]['ndcg100'].append(
            NDCG(a1_e1, qrels, answer['id'], 100))
        scores['approach1'][3]['ndcg10'].append(
            NDCG(a1_e3, qrels, answer['id'], 10))
        scores['approach1'][3]['ndcg100'].append(
            NDCG(a1_e3, qrels, answer['id'], 100))
        scores['approach1'][5]['ndcg10'].append(
            NDCG(a1_e5, qrels, answer['id'], 10))
        scores['approach1'][5]['ndcg100'].append(
            NDCG(a1_e5, qrels, answer['id'], 100))
        scores['approach1'][10]['ndcg10'].append(
            NDCG(a1_e10, qrels, answer['id'], 10))
        scores['approach1'][10]['ndcg100'].append(
            NDCG(a1_e10, qrels, answer['id'], 100))

        # aproach 2
        scores['approach2'][0]['ndcg10'].append(
            NDCG(a2_e0, qrels, answer['id'], 10))
        scores['approach2'][0]['ndcg100'].append(
            NDCG(a2_e0, qrels, answer['id'], 100))
        scores['approach2'][1]['ndcg10'].append(
            NDCG(a2_e1, qrels, answer['id'], 10))
        scores['approach2'][1]['ndcg100'].append(
            NDCG(a2_e1, qrels, answer['id'], 100))
        scores['approach2'][3]['ndcg10'].append(
            NDCG(a2_e3, qrels, answer['id'], 10))
        scores['approach2'][3]['ndcg100'].append(
            NDCG(a2_e3, qrels, answer['id'], 100))
        scores['approach2'][5]['ndcg10'].append(
            NDCG(a2_e5, qrels, answer['id'], 10))
        scores['approach2'][5]['ndcg100'].append(
            NDCG(a2_e5, qrels, answer['id'], 100))
        scores['approach2'][10]['ndcg10'].append(
            NDCG(a2_e10, qrels, answer['id'], 10))
        scores['approach2'][10]['ndcg100'].append(
            NDCG(a2_e10, qrels, answer['id'], 100))

    # calculate average
    scores['approach1'][0]['ndcg10'] = sum(
        scores['approach1'][0]['ndcg10'])/len(scores['approach1'][0]['ndcg10'])
    scores['approach1'][0]['ndcg100'] = sum(
        scores['approach1'][0]['ndcg100'])/len(scores['approach1'][0]['ndcg100'])
    scores['approach1'][1]['ndcg10'] = sum(
        scores['approach1'][1]['ndcg10'])/len(scores['approach1'][1]['ndcg10'])
    scores['approach1'][1]['ndcg100'] = sum(
        scores['approach1'][1]['ndcg100'])/len(scores['approach1'][1]['ndcg100'])
    scores['approach1'][3]['ndcg10'] = sum(
        scores['approach1'][3]['ndcg10'])/len(scores['approach1'][3]['ndcg10'])
    scores['approach1'][3]['ndcg100'] = sum(
        scores['approach1'][3]['ndcg100'])/len(scores['approach1'][3]['ndcg100'])
    scores['approach1'][5]['ndcg10'] = sum(
        scores['approach1'][5]['ndcg10'])/len(scores['approach1'][5]['ndcg10'])
    scores['approach1'][5]['ndcg100'] = sum(
        scores['approach1'][5]['ndcg100'])/len(scores['approach1'][5]['ndcg100'])
    scores['approach1'][10]['ndcg10'] = sum(
        scores['approach1'][10]['ndcg10'])/len(scores['approach1'][10]['ndcg10'])
    scores['approach1'][10]['ndcg100'] = sum(
        scores['approach1'][10]['ndcg100'])/len(scores['approach1'][10]['ndcg100'])

    scores['approach2'][0]['ndcg10'] = sum(
        scores['approach2'][0]['ndcg10'])/len(scores['approach2'][0]['ndcg10'])
    scores['approach2'][0]['ndcg100'] = sum(
        scores['approach2'][0]['ndcg100'])/len(scores['approach2'][0]['ndcg100'])
    scores['approach2'][1]['ndcg10'] = sum(
        scores['approach2'][1]['ndcg10'])/len(scores['approach2'][1]['ndcg10'])
    scores['approach2'][1]['ndcg100'] = sum(
        scores['approach2'][1]['ndcg100'])/len(scores['approach2'][1]['ndcg100'])
    scores['approach2'][3]['ndcg10'] = sum(
        scores['approach2'][3]['ndcg10'])/len(scores['approach2'][3]['ndcg10'])
    scores['approach2'][3]['ndcg100'] = sum(
        scores['approach2'][3]['ndcg100'])/len(scores['approach2'][3]['ndcg100'])
    scores['approach2'][5]['ndcg10'] = sum(
        scores['approach2'][5]['ndcg10'])/len(scores['approach2'][5]['ndcg10'])
    scores['approach2'][5]['ndcg100'] = sum(
        scores['approach2'][5]['ndcg100'])/len(scores['approach2'][5]['ndcg100'])
    scores['approach2'][10]['ndcg10'] = sum(
        scores['approach2'][10]['ndcg10'])/len(scores['approach2'][10]['ndcg10'])
    scores['approach2'][10]['ndcg100'] = sum(
        scores['approach2'][10]['ndcg100'])/len(scores['approach2'][10]['ndcg100'])

    with open(output_file, 'w') as outfile:
        json.dump(scores, outfile)
