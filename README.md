Enterprise  Public Opinion Mining System
==========================

## Requirements
1. MySQL
2. Apache Spark

## Installation
1. Install package requirements.

```
pip install -r requirements.txt
```

2. Downloads NLTK corpus.
```
./setup/nltk.py
```


## Tasks
### Content Extraction and Name Recognition
#### Related files
```
- epoms/news_extraction.py
- epoms/entity_extract.py
- epoms/linguistic_utility.py
- scripts/extract-news.py
```

#### Action
```
python scripts/extract-news.py  <part_to_source_directory>
```

### Pagerank computing
#### Related files
```
- scripts/name-graph-pagerank.py
- scripts/pagerank.py
- scripts/json-name-flare-graph.py
- web/flare-name.html
- web/flare-name.js
- web/data/*
```

#### Action
```
# Evaluation
./scripts/evaluation-pagerank.sh <case_name> <how_many_sentences_to_form_relationship or all>

# View the result
cd web && python -m SimpleHTTPServer &&

# Then open http://localhost:8000/flare-name.html?file=data/<case_name>
```
