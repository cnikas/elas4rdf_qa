# Νίκος Γουνάκης QA Worklog

# DistilBERT
` a distilled version of BERT: smaller, faster, cheaper and lighter`

## Performance in first 100 Questions 

### Threshold = 0.5

```json
{
  "precision": 12.417802693744532,
  "recall": 33.813604897568936,
  "f1": 14.826156232800765,
  "accuracy": 44.943820224719104,
  "total": 89
}
```

```json
{
   "Total time": 1118.6738255023956
}
```

## Performance in 2039 Questions (All)

### Threshold = 0.5

```json
{
  "precision": 10.462711811370637,
  "recall": 26.261639633607412,
  "f1": 12.098216193776183,
  "accuracy": 42.986666666666665,
  "total": 1875
}
```

```json
{
  "Total time": 31492.684856414795
}
```

## Problems

 Questions: 
 * id:18 `who plays bilbo baggins in the hobbit?`
 * id:71 `who is moira en x men?` 
 * id:77 `what works of art did leonardo da vinci produce?`
 <br>leads to error:
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or
	there is an error in the application.</p>
```
gunicorn_error.log
```
[2021-03-13 15:14:05,686] ERROR in app: Exception on /answer [GET]
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/flask/app.py", line 2447, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/local/lib/python3.6/dist-packages/flask/app.py", line 1952, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/local/lib/python3.6/dist-packages/flask/app.py", line 1821, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/usr/local/lib/python3.6/dist-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/usr/local/lib/python3.6/dist-packages/flask/app.py", line 1950, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/local/lib/python3.6/dist-packages/flask/app.py", line 1936, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/home/nicolaig/elas4rdf_qa/app.py", line 29, in api_answer
    entities = get_entities_from_elas4rdf(question)
  File "/home/nicolaig/elas4rdf_qa/entity_expansion.py", line 111, in get_entities_from_elas4rdf
    entities = [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in response_json['results']['entities']]
  File "/home/nicolaig/elas4rdf_qa/entity_expansion.py", line 111, in <listcomp>
    entities = [{'uri':e['entity'],'rdfs_comment':e['ext']['rdfs_comment']} for e in response_json['results']['entities']]
KeyError: 'rdfs_comment'
```

Error : `a key is missing form elasS4RDF response`
<br>
Possible Fixes: 
* `add a blank "rdfs_comment" : "[]"`
* `stop using entities`

Status: `FIXED`
