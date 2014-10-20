#Skill mapping API 

This is an API that given a Job ID will return matched Skills. 

##Usage:

To fire up the API, run 

`python server.py`

## Tests 

Under `unittests/` run `python test_server.py`

##Dependencies

* A job description call: The API makes a call with the `job_id` to get the  job description text. This could be a database call, but in the `method=local` context, it read it off the local file `/model/job_desc.json`
* Skill to feature map:   `model/skillname_to_skilltags.tsv`  
	* Each line in file has the format `skill name:keyword_1,keyword_2,....,keyword_n`. e.g. `sales skills:sale,sales,selling,retail`
* Stop words: `/ model / skill_stop_words.txt` provides a way  to ignore or blacklist words in the vectorization steps.

## Call and  Response:

The API is called with a `json` payload of the format:
`{"job_id": "10000038"}`


If the job id/description is not found, the API returns an error 
` ERROR: job text could not be retrieved`

If the job description could be retrieved and skills could be matched, it returns a response like:

```Response:
  {"0": {"skill": "interpersonal and communication skills", "score": 2, "matched_tags": ["communication", "interpersonal"]}, "1": {"skill": "sales skills", "score": 4, "matched_tags": ["selling", "retail", "sale", "sales"]}}
```

Here, two skills could be matched to the job, namely "interpersonal and communication skills"  and "sales skills". It also shows which keywords matched the description and a score (number of matched keywords) for further introspection. 
