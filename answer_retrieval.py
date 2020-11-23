import requests
import json

def get_entities(query_string,size):
    payload = {
        "type" : "entities",
        "query" : query_string,
        "size" : 100
    }
    url = "https://demos.isl.ics.forth.gr/elas4rdf/entities_json"
    response = requests.get(url,params=payload)
    return [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in response.json()['results']['entities'][0:size]]

def annotate_spotlight(query):
    payload = {
        "text" : query
    }
    url = "https://api.dbpedia-spotlight.org/en/annotate"
    response = requests.get(url,params=payload)
    if "Resources" in response:
        return response["Resources"][0]["@URI"]
    else:
        return ""
    
def sparql_query(query_string):
    url = "http://139.91.183.46:8899/sparql"
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

def get_entity_types(entity_uri):
    types = []
    query_string = ("select ?t1 where {{"
                    "<{}> rdf:type ?t1 . "
                    "}}"
                    ).format(entity_uri)
    response = sparql_query(query_string)
    for r in response:
        types.append(r['t1'])
    return list(map(lambda x: x[x.rindex('/')+1:],types))

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
    for r in response:
        r['entity'] = entity_uri 
    return response

def objects_in_range(entity_uri):
    query_string = ("select ?answer ?answerType where {{"
                        "<{}> ?p ?answer . "
                        "?p rdfs:range ?answerType . "
                        "?p rdfs:label ?predicateLabel . "
                        "FILTER(isLiteral(?answer)) "
                        "FILTER(lang(?answer) = 'en' || lang(?answer) = '') "
                    "}}").format(entity_uri)         
    response = sparql_query(query_string)          
    for r in response:
        r['entity'] = entity_uri 
    return response



if __name__ == "__main__":
    #print(objects_of_type("http://dbpedia.org/resource/Greece","http://dbpedia.org/ontology/Work"))
    #print(objects_in_range("http://dbpedia.org/resource/Greece"))
    print(get_entity_types("http://dbpedia.org/resource/Greece"))
    #for r in response['results']['bindings']
    #    r['sl']['value']
    