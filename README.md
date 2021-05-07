# frutafeia

Fruta Feia Django API :cherries: :tangerine: :watermelon:

## SETUP

- The libraries required and their versions are listed in the `requirements.txt` file.
  Run the following commands to setup environment:

_WINDOWS_

```bash
    git clone https://github.com/franciscobmacedo/frutafeia.git
    cd  frutafeia
    py -m venv venv
    .\venv\scripts\activate
    pip install -r requirements.txt
    py manage.py migrate
```

_MAC/LINUX_

```bash
    git clone https://github.com/franciscobmacedo/frutafeia.git
    cd  frutafeia
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
```

<br />

## Run

```bash
    python manage.py runserver
```

Open http://localhost:8000/ on your browser and enjoy :wink:
