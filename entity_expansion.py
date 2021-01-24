import requests
import json

"""This module contains methods to retrieve
RDF nodes that match the answer type to a question
and generate sentences to extend entity descriptions
"""

def sparql_query(query_string):
    # Execute a query on a SPARQL endpoint
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
        keys = response_json['head']['vars']
        results = []
        for b in response_json['results']['bindings']:
            result = {}
            for k in keys:
                result[k] = b[k]['value']
            results.append(result)
    except json.decoder.JSONDecodeError:
        print("sparql error")
        results = [] 
    return results

def resource_sentences(entity_uri,type_uri):
    """ Find subjects of the entity that match the answer type
    and generate sentences of the form "entity predicate label answer"
    """
    sentences = []
    query_string_o = ("select distinct str(?pl) as ?pLabel ?a where {{"
                        "<{0}> ?p ?a . "
                        "?p rdfs:label ?pl . "
                        "<{1}> owl:equivalentClass ?eq . "
                        "?a rdf:type ?eq . "
                        "FILTER(lang(?pl) = 'en' || lang(?pl) = '') "
                    "}}").format(entity_uri,type_uri)
    response = sparql_query(query_string_o)
    if len(response)>20:
    	response = response[0:20]
    for r in response:
        sentences.append(entity_to_str(entity_uri)+' '+r['pLabel']+' '+entity_to_str(r['a']))
    return sentences

def literal_sentences(entity_uri,literal_type):
    """ Find literal subjects of the entity that match
    the answer type and generate sentences of the form
    "entity predicate label answer"
    """
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
        if len(response)>20:
    	    response = response[0:20]
        for r in response:
            if len(r['a'])<100:
                isNumber = r['a'].replace('.','',1).isdigit()
                if(literal_type == 'number' and isNumber):
                    sentences.append(entity_string+' '+r['pLabel']+' '+r['a'])
                elif(literal_type =='string' and (not isNumber)):
                    sentences.append(entity_string+' '+r['pLabel']+' '+r['a'])

    return sentences

def entity_to_str(e):
    # convert a dbpedia uri to a readable string
    return e[e.rindex("/")+1:].replace('_',' ')
