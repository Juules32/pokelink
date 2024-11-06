# pokelink
Welcome to the repo for PokéLink, the daily pokemon-themed puzzle game!

Visit the page [here](https://pokelink.vercel.app)!

## Local Setup

### Backend

- As a prerequisite, you need to have a postgres database running.

- Copy the connection string and paste it into a copy of `.env.example`, which you should rename 
to `.env`. Leave the other environment variables as they are.

- Go into the `backend` folder.

- Run this to install dependencies:

```pip install```

- Run this to generate pokemon JSON data used to generate graph data:

```python pokemon_data_generation.py```

- Run this to generate graph data:

```python graph_data_generation.py```

- Run this to set up your database tables etc.:

```python setup.py```

- Run this to start a local webserver:

```uvicorn main:app --reload --port 80```

- Visit [localhost/docs](http://localhost/docs) to see if the backend is running.

### Frontend

- Go into the `frontend` folder.

- Run this to install dependencies:

```npm i```

- Run the following to start a webserver set to run by default on port `5173`.

- Visit [localhost:5173](http://localhost:5173) to see if the frontend is running.

## Production Setup

I deployed the app to vercel. Feel free to choose another option.

- Create a vercel postgres database.

- Set up the tables etc. by changing `CONNECTION_STRING` in `.env` to the new connection string temporarily
and run the `setup.py` script in the `backend` folder.

- Create a vercel blob storage.

- For the frontend and backend respectively, add a new project on vercel. Set the root folder
to backend/frontend.

- On the backend project, set up environment variables for `CRON_SECRET` (can be whatever), `CONNECTION_STRING` (from the vercel database), `ENVIRONMENT` ("PRODUCTION") and `BLOB_HOST` (from the vercel blob storage).

- On the frontend project, set up environment variable for `PUBLIC_BACKEND_HOST` ("https://pokelink-backend.vercel.app" or something similar).
