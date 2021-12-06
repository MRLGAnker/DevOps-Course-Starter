# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change).

## Add MongoDB details to .env file
Add the following to the .env file:
MONGO_USERNAME=<MongoDB Username>
MONGO_PASSWORD=<MongoDB Password>
MONGO_URL=<MongoDB URL>
MONGO_DATABASE=<MongoDB Database>

## Add OAuth details to .env file
Add the following to the .env file:
OAUTH_CLIENT_ID=<OAuth Client ID>
OAUTH_CLIENT_SECRET=<OAuth Client Secret>

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Running the Tests

To run the tests requires pytest to be installed, if you have run through the Dependencies step it should have been installed when you ran 'poetry install'.

You can then run: "poetry run pytest" to execute all the currently defined tests.

## Using Docker containers

Download: 
* Docker - you'll need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Installation instructions for Windows can be found [here](https://docs.docker.com/docker-for-windows/install/). If prompted to choose between using Linux or Windows containers during setup, make sure you choose Linux containers.

### Running the Containers

#### Dev Container
* Enables Flask's debugging/developer modes

##### Build
```bash
$ docker build --target development --tag todo-app:dev .
```
##### Run
```bash
$ docker run --env-file .env -p 5000:5000 -v "$(pwd)/todo_app:/DevOps-Course-Starter/todo_app" todo-app:dev
```

#### Test Container
* Runs the tests in the test & test_e2e folders

##### Build
```bash
$ docker build --target test --tag todo-app:test .
```
##### Run
```bash
$ docker run --env-file .env -p 5000:5000 todo-app:test
```

#### Prod Container

##### Build
```bash
$ docker build --target production --tag todo-app:prod .
```
##### Run
```bash
$ docker run --env-file .env -p 5000:5000 todo-app:prod
```