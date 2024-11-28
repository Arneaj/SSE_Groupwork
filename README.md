# gm_app
## Game Master Helper App

## Pre
Make sure you have Python3 on your machine.

## Running the app
To run the app:
```bash
python3 venv venv
source venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
export FLASK_APP=gmapp/app.py
export FLASK_ENV=development
flask run
```

Now please browse to <http://localhost:5000> to see the app live.
