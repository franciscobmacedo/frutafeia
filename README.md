# frutafeia :cherries: :tangerine: :watermelon:

Fruta Feia Django API

## SETUP
- You need to store a file with the google cloud credentials in `gsheets/keys.json`. Go to https://console.cloud.google.com for more.
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

## FILL DATABASE

To fill your database with data from google sheets (remember, you need the file `keys.json` in the directory `gsheets`)

To fill the table `Produtor`:
```bash
    python manage.py tasks -produtor
```

To fill the table `Produto`:
```bash
    python manage.py tasks -produto
```

To fill the table `Disponibilidade`:
```bash
    python manage.py tasks -disponibilidade
```

## RUN

```bash
    python manage.py runserver
```

Open http://localhost:8000/ on your browser and enjoy :wink:


## API

These are the API endpoints and their description.

- `/api/` Main endpoint. lists all enpoints
    - `/api/produtores/` lists all produtores
    - `/api/produtos/` lists all produtos
    - `/api/disponibilidades/` lists all disponibilidades


## TODO
- Quantidade de cestas a fazer
- Produtos Quantidades de referencia
- Sazonalidade de Produtos (inteiro, produto, float)


