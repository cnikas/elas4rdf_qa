import requests
import json

def get_entities(query_string,size):
    payload = {
        "type" : "entities",
        "query" : query_string,
        "size" : size
    }
    url = "https://demos.isl.ics.forth.gr/elas4rdf/entities_json"
    response = requests.get(url,params=payload)
    return [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in response.json()['results']['entities'][0:size]]

def get_entities_updated(selected_entities,selected_type):
    ### get neighbor entities matching answer type ###
    selected_type_uri = "http://dbpedia.org/ontology/"+selected_type
    new_entities = []
    for se in selected_entities:
        new_entities.extend(objects_of_type(se,selected_type_uri))
    return new_entities
    
def sparql_query(query_string):
    #url = "http://139.91.183.46:8899/sparql"
    url = "http://dbpedia.org/sparql"
    payload = {
        "query": query_string,
        "default-graph-uri": "http://dbpedia.org"
    }
    headers = {"Accept":"application/json"}
    response = requests.get(url,params=payload,headers=headers)
    try:
        response_json =  response.json()
    except json.decoder.JSONDecodeError:
        print(query_string) 
    keys = response_json['head']['vars']
    results = []
    for b in response_json['results']['bindings']:
        result = {}
        for k in keys:
            result[k] = b[k]['value']
        results.append(result)
    return results

def objects_of_type(entity_uri,type_uri):
    query_string_o = ("select ?answer ?rdfsComment where {{"
                        "<{0}> ?p ?answer . "
                        "?answer rdf:type <{1}> . "
                        "?answer rdfs:comment ?rdfsComment . "
                        "FILTER(lang(?predicateLabel) = 'en' || lang(?predicateLabel) = '') "
                    "}}").format(entity_uri,type_uri)
    query_string_s = ("select ?answer ?rdfsComment where {{"
                        "?answer ?p <{0}> . "
                        "?answer rdf:type <{1}> . "
                        "?answer rdfs:comment ?rdfsComment . "
                    "}}").format(entity_uri,type_uri)
    response = sparql_query(query_string_o)
    response.extend(sparql_query(query_string_s))
    entities = []
    for r in response:
        if(r['answer'].startswith("http")):
            entities.append({
                "uri":r['answer'],
                "rdfs_comment":r['rdfsComment']
            })
    return entities