# Real-time Chat Server

## Running Locally

This project depends on the [profanity filter microservice](https://github.com/kylemadkins/profanity-filter), as well as the [profanity filter protocol buffer files](https://github.com/kylemadkins/profanity-filter-protos), which are included in this project as a Git submodule. Once you have the profanity filter microservice up and running via `docker-compose`, follow the steps below

1. Copy the `sample.env` file to a regular `.env` file
2. Spin up the containers with `docker-compose up` as usual. This will start Redis and an API server at port 8000
3. Go to /docs to see the documentation
