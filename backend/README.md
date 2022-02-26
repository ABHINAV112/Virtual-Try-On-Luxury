# Api for clothe fitting

## Setup

1. make env
```bash
virtualenv env
```

2. pip install
```bash
pip3 install -r requirements.txt
```

3. make config file and add following values
```bash
touch config.py
```
Add the following values
```
HUMAN_PARSING_MODELS_PATH="<location of human parsing squeezenet>"
OPENPOSE_BASEURL="<location of open pose github repo>"
```