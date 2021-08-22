# Analyze cases that fail

## Plan

* run evaluation
* take system output
* see if gold tokens can be found in the text where extractive QA finds the answer
* then decide what is failing


at the same time we calculate accuracy we also calculate the ideal accuracy. 
Ideal accuracy is the accuracy the system would achieve if the answer extraction was perfect. To calculate it we collect all the texts which the answers were extracted and then we check if at least one `gold_token` can be found in the text.

To determine which system component is the most responsible (`pipeline` or `elas4rdf entinty search`) we calculate the percantage of the improvement each component needs to be perfect.
At the `json` below we can see that the `accuracy` is `60.285` and the `ideal_accuracy` is `77.362`.
The improvement for the pipeline is calculated as:

$$
pipeline\_improvement = \frac{ideal\_accuracy}{accuracy} = \frac{77.362}{60.285} = 28.3\%
$$
the pipe line needs `28.3%` improvement to be perfect. As for the entity search the improvement is calculated as:

$$
entity\_search\_improvement = \frac{100}{ideal\_accuracy} = \frac{100}{77.362} = 29.2\% 
$$

In our case the entity search has slightly bigger gap for improvement so it is to blame.

```json
{
  "precision": 5.589868610284863,
  "recall": 37.005099614374195,
  "f1": 9.712585940378899,
  "micro_f1": 8.629797127697836,
  "accuracy": 60.28543307086614,
  "ideal_accuracy": 77.36220472440945,
  "total": 2032,
  "failed": 39.71456692913386,
  "query average time": 0.0
}
Failed: 807
Average Query Time: 0.0
```