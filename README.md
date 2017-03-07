# qbotio-resources

## Applications

- process_query.py: Example of applying NLTK techniques to improve a input query
- corpus_to_json.py: Convert a sample corpus to JSON. See sample_corpus/ for example formats that the application can parse
- eval_from_json: Evaluate a training set from a JSON file against Q Bot IO search endpoint
- compare_eval.py: Compare between two evaluations
- extract_from_json: Extract questions or answers from JSON corpus

## Development

### Git Setup

Clone the git repository: ```$ git clone https://github.com/techcats/qbotio-resources.git```

### Environment Setup

1. Install [python 3.6+](https://www.python.org/)
2. Install/Upgrade [pip](https://pip.pypa.io/en/stable/installing/)
3. Install virtualenv: ```$ pip install virtualenv```
4. Install virtualenvwrapper. Follow and see usage with [Windows](https://pypi.python.org/pypi/virtualenvwrapper-win), [Linux & Mac](https://virtualenvwrapper.readthedocs.io/en/stable/) guides.
6. Create (```$ mkvirtualenv qbotio-resources```) and work (```$ workon qbotio-resources```) on a local environment using virtualenvwrapper.
7. Set the default project directory: ```(qbotio-resources) $ setvirtualenvproject $VIRTUAL_ENV <path to cloned repo>``` (Linux & Mac) or use ```setprojectdir <path to cloned repo>``` (Windows)
8. ```(qbotio-resources) $ deactivate```
9. ```$ workon qbotio-resources```

You should now be at the root directory of 'qbotio-resources/'. Calling ```$ workon qbotio-resources``` should now automatically direct to the your sources directory.

> A tip for step 3 & 4 (Linux & Mac): Similiar to ```python3```, ```pip3``` is the python 3.x's equivalent. virtualenvwrapper.sh may require the correct python version in your "VIRTUALENVWRAPPER_PYTHON" environment variable.

### Install/Update python libraries

Run ```(qbotio-resources) $ pip install -r requirements.txt```

> To include a new library use ```(qbotio-resources) $ pip install [package]```, and then ```(qbotio-resources) $ pip freeze > requirements.txt```

### Install NLTK Data

```bash
python -m nltk.downloader stopwords
python -m nltk.downloader punkt
```
> If there are errors while you install NLTK data, you can manual download from [here](http://www.nltk.org/nltk_data/)
And put data to: 
```
Windows: C:\nltk_data\tokenizers
OSX: /usr/local/share/nltk_data/tokenizers
Unix: /usr/share/nltk_data/tokenizers
```

