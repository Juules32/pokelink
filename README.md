# pokelink
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
