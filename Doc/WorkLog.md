# Νίκος Γουνάκης QA Worklog

# DistilBERT
` a distilled version of BERT: smaller, faster, cheaper and lighter`

## Performance in first 100 Questions (using entity)
Threshold = 0.5

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

## Performance in all 2039 Questions (using entity)
Threshold = 0.5

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

## Performance in all 2039 Questions including all Thresholds (using entity)

| Threshold | 0.0    | 0.1    | 0.2    | 0.3    | 0.4    | 0.5    | 0.6    | 0.7    | 0.8    | 0.9    |
| --------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Precision | 5.589  | 6.967  | 7.831  | 8.588  | 9.361  | 10.462 | 11.278 | 11.843 | 13.291 | 15.375 |
| Recall    | 37.005 | 34.310 | 32.613 | 30.340 | 28.228 | 26.261 | 24.473 | 23.100 | 21.936 | 20.831 |
| F1        | 37.005 | 9.936  | 10.742 | 11.145 | 11.563 | 12.098 | 12.386 | 12.568 | 13.313 | 14.455 |
| Accuracy  | 60.285 | 55.857 | 53.339 | 50.000 | 46.173 | 42.986 | 39.615 | 37.361 | 35.334 | 33.042 |


# RoBERTa
`A Robustly Optimized BERT Pretraining Approach`

## Performance in first 100 Questions (using entity)
Threshold = 0.5
```json
{
  "precision": 19.95683879612451,
  "recall": 34.49843873636149,
  "f1": 20.490980151118404,
  "accuracy": 46.42857142857143,
  "total": 84
}
```
```json
{
  "Total time": 1293.2600502967834
}
```

## Performance in all 2039 Questions (using entity)
Threshold = 0.5
```json
{
  "precision": 23.48773853717954,
  "recall": 29.556822610929405,
  "f1": 26.175083984083653,
  "accuracy": 46.13180515759312,
  "total": 1047
}
```
```json
{
  "Total time": 29254.313611507416
}
```

## Performance in all 2039 Questions including all Thresholds (using entity)

| Threshold | 0.0    | 0.1    | 0.2    | 0.3    | 0.4    | 0.5    | 0.6    | 0.7    | 0.8    | 0.9    |
| --------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Precision | 6.192  | 14.879 | 17.348 | 19.483 | 21.109 | 23.487 | 26.509 | 28.844 | 30.983 | 36.480 |
| Recall    | 37.284 | 32.198 | 30.970 | 30.183 | 29.426 | 29.556 | 30.435 | 30.300 | 31.797 | 33.940 |
| F1        | 10.621 | 20.353 | 22.239 | 23.680 | 24.583 | 26.175 | 28.337 | 29.554 | 31.385 | 35.164 |
| Accuracy  | 60.826 | 51.352 | 48.714 | 47.357 | 46.104 | 46.131 | 47.514 | 47.555 | 47.649 | 50.400 |

# Problems

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