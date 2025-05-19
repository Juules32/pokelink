# PokéLink 🐲
Welcome to the repo for PokéLink, the daily pokemon-themed puzzle game!

Visit the page [here](https://pokelink.juules32.com)!

# Local Setup

## Backend

- Have a postgres database running.
- Navigate to `/backend`
- Copy `.env.example` to `.env.development` and fill in the values
- Run the following copmmands:
```
pip install -r requirements.txt                 # Install dependencies
python pokemon_data_generation.py               # Generate pokemon JSON data from pokeAPI
python graph_data_generation.py                 # Generate graph from pokemon data
python setup.py                                 # Generate tables and template puzzles on the DB
uvicorn main:app --reload --port 80             # Run the webserver
```

- Visit [localhost/docs](http://localhost/docs) to see if the backend is running.

## Frontend

- Navigate to `/frontend`
- Copy `.env.example` to `.env.development` and fill in the values
- Run the following copmmands:
```
npm i                                           # Install dependencies
npm run dev                                     # Run the webserver
```

- Visit [localhost:5173](http://localhost:5173) to see if the frontend is running.

# Production Setup on Ubuntu Server

## Backend

- Have a postgres database running
- Have a local file server (blob) running as a service by using nginx
- Navigate to `/backend`:
- Copy `.env.example` to `.env.production` and fill in the values
- Run the following copmmands:
```
sudo apt install python3-venv python3-full      # Install venv
python3 -m venv .venv                           # Make a venv folder
source .venv/bin/activate                       # Go into the venv                
pip install -r requirements.txt                 # Install requirements
python pokemon_data_generation.py               # Generate pokemon data in json
python graph_data_generation.py                 # Generate graph and store as .json and .pkl
python setup.py                                 # Requires a working connection string to the postgres database
uvicorn main:app --port <port> --env-file .env.production # Start the webserver
```
- Copy the pickled graph data to the file server directory (for example `/srv/pokelink-backend-blob`)

## Frontend

- Navigate to `/frontend`
- Copy `.env.example` to `.env.production` and fill in the values
- Run the following copmmands:
```
npm i                                           # Install dependencies
npm run build                                   # Build the production files
PORT=<port> node build                          # Host the production files
```

## Creating of Services

### Backend

- Create a service file:
```sudo nano /etc/systemd/system/pokelink-backend.service```

- Enter:
```
[Unit]
Description=Pokelink Backend (Uvicorn) Service
After=network.target

[Service]
User=<user>
WorkingDirectory=<repo path>/backend
ExecStart=<repo path>/backend/.venv/bin/uvicorn main:app --port <port> --env-file .env.production
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Run the following commands:
```
sudo systemctl start pokelink-backend
sudo systemctl enable pokelink-backend
sudo systemctl status pokelink-backend
```

### Frontend

- Create a service file:
```sudo nano /etc/systemd/system/pokelink-frontend.service```

- Enter:
```
Description=Pokelink Frontend Service
After=network.target

[Service]
User=<user>
WorkingDirectory=<repo path>/frontend
ExecStart=/usr/bin/env PORT=<port> node build
Restart=on-failure
EnvironmentFile=<repo path>/.env.production

[Install]
WantedBy=multi-user.target
```

Run the following commands:
```
sudo systemctl start pokelink-frontend
sudo systemctl enable pokelink-frontend
sudo systemctl status pokelink-frontend
```

### Blob

- Install nginx and enable it as a service
- Run:
```sudo nano /etc/nginx/sites-available/pokelink-production-blob```

- Enter:
```
server {
    listen 127.0.0.1:<port>;

    root <blob path>;
    autoindex on;
    charset utf-8;

    location / {
        try_files $uri $uri/ =404;
    }

    access_log /var/log/nginx/pokelink_production_blob_access.log;
    error_log /var/log/nginx/pokelink_production_blob_error.log;
}
```

- Run the following commands:
```
sudo ln -s /etc/nginx/sites-available/pokelink-production-blob /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
sudo systemctl status nginx
```

### Postgres DB
[Documentation here](https://documentation.ubuntu.com/server/how-to/databases/install-postgresql/index.html)
