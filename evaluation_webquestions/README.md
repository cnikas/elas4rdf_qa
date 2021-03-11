This folder contains data and scripts used to evaluate the system over the [WebQuestions](https://worksheets.codalab.org/worksheets/0xba659fe363cb46e7a505c5b6a774dc8a) collection.

Files:
* `webquestions.test.json` WebQuestions test collection
* `convert.py` Script to convert the collection to the format used by the other scripts
* `webquestions_test_converted.json` The collection converted using `convert.py`
* `get_system_output.py` script to obtain answers for all the questions in the collection (takes a long time to complete)
* `system_output.json` The output obtained by `get_system_output.py`
* `filter_system_output.py` Script used to keep answers with a score equal or higher than a given threshold
* `system_output_filtered.json` Output of `filter_system_output.py`
* `evaluate.py` Script used to obtain evaluation scores