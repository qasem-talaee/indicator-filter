# Coinex Indicator Filter

This project get list of all coins in coinex.then it checks all currencies according to the given strategy and sends you the signal via email.

## Installation
Get the project source and open terminal in source directory and enter

```bash
python3 -m venv .venv
```
then
```bash
source ./venv/bin/activate
```
then
```bash
pip install -r req.txt
```
and finaly run it
```
python3 main.py
```

## Setup your information
* setup your filter strategy in lib/indicator.py
* setup your email and password in lib/send_email.py