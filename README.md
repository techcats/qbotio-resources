# qbotio-resources

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
8. ```(qbotio) $ deactivate```
9. ```$ workon qbotio```

You should now be at the root directory of 'qbotio-resources/'. Calling ```$ workon qbotio``` should now automatically direct to the your sources directory.

> A tip for step 3 & 4 (Linux & Mac): Similiar to ```python3```, ```pip3``` is the python 3.x's equivalent. virtualenvwrapper.sh may require the correct python version in your "VIRTUALENVWRAPPER_PYTHON" environment variable.

### Install/Update python libraries

Run ```(qbotio) $ pip install -r requirements.txt```

> To include a new library use ```(qbotio) $ pip install [package]```, and then ```(qbotio) $ pip freeze > requirements.txt```