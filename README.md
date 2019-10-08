# messenger-to-elastic
Export messenger exported data to elasticsearch

## Get the data

On facebook, go to parameters -> Your facebook data -> Download your data
Select the JSON format, and the lowest photo quality.
Make sure to uncheck all boxes but the messenger one, and download your
report.

## Setup the env

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

configure your elasticseearch endpoint in config.py

Run the script with something like :
find <path to extracted data> | grep json | xargs ./main.py
