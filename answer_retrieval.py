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
        print("sparql error") 
    keys = response_json['head']['vars']
    results = []
    for b in response_json['results']['bindings']:
        result = {}
        for k in keys:
            result[k] = b[k]['value']
        results.append(result)
    return results

def resource_sentences(entity_uri,type_uri):
    sentences = []
    query_string_o = ("select str(?pl) as ?pLabel ?a where {{"
                        "<{0}> ?p ?a . "
                        "?a rdf:type <{1}> . "
                        "?p rdfs:label ?pl . "
                        "FILTER(lang(?pl) = 'en' || lang(?pl) = '') "
                    "}}").format(entity_uri,type_uri)
    response = sparql_query(query_string_o)
    for r in response:
        sentences.append(entity_to_str(entity_uri)+' '+r['pLabel']+' '+entity_to_str(r['a']))
    #query_string_s = ("select str(?pl) as ?pLabel ?a where {{"
    #                    "?a ?p <{0}> . "
    #                    "?a rdf:type <{1}> . "
    #                    "?p rdfs:label ?pl . "
    #                    "FILTER(lang(?pl) = 'en' || lang(?pl) = '') "
    #                "}}").format(entity_uri,type_uri)
    #response = sparql_query(query_string_s)
    #for r in response:
    #    sentences.append(entity_to_str(r['a'])+' '+r['pLabel']+' '+entity_to_str(entity_uri))
    return sentences

def literal_sentences(entity_uri,literal_type):
    sentences = []
    entity_string = entity_to_str(entity_uri)
    if literal_type == 'date':
        query_string = ("select str(?answer) as ?a str(?pl) as ?pLabel where {{"
                        "<{}> ?p ?answer . "
                        "?p rdfs:range xsd:date . "
                        "?p rdfs:label ?pl . "
                        "FILTER(isLiteral(?answer)) "
                        "FILTER(lang(?pl) = 'en' || lang(?pl) = '') "
                        "}}").format(entity_uri)  
        response = sparql_query(query_string)                 
        for r in response:
            sentences.append(entity_string+' '+r['pLabel']+' '+r['a'])
    else: # if number or string
        query_string = ("select str(?answer) as ?a str(?pl) as ?pLabel where {{"
                        "<{}> ?p ?answer . "
                        "?p rdfs:range ?answerType . "
                        "?p rdfs:label ?pl . "
                        "FILTER(isLiteral(?answer)) "
                        "FILTER(lang(?pl) = 'en' || lang(?pl) = '') "
                        "}}").format(entity_uri)         
        response = sparql_query(query_string)   
        for r in response:
            if len(r['a'])<100:
                isNumber = r['a'].replace('.','',1).isdigit()
                if(literal_type == 'number' and isNumber):
                    sentences.append(entity_string+' '+r['pLabel']+' '+r['a'])
                elif(literal_type =='string' and (not isNumber)):
                    sentences.append(entity_string+' '+r['pLabel']+' '+r['a'])

    return sentences

def entity_to_str(e):
    return e[e.rindex("/")+1:].replace('_',' ')

if __name__ == '__main__':
    print(resource_sentences('http://dbpedia.org/resource/Greece','http://dbpedia.org/ontology/Person'))
    print(literal_sentences('http://dbpedia.org/resource/Greece','date'))
    print(literal_sentences('http://dbpedia.org/resource/Greece','number'))
    print(literal_sentences('http://dbpedia.org/resource/Greece','string'))

