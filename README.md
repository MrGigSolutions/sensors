# Sensor Reporting Simulation
This project is an oversimplified simulation of a reporting dashboard for 
reporting sensor readings.

The project consists of 5 main parts:
- The sensor: this is a Celery-based scheduler that schedules a sensor reading every 30 seconds.
- The broker: used by Celery for task scheduler. In this project, it's RabbitMQ.
- The backend: this receives sensor readings, and allows the frontend to
  request report data, and to authenticate a user.
- The database: A Postgres database
- The frontend: a simple React app that reads the sensor data from the backend, and allows
  the user to login. The graph refreshes every 60 seconds.

## Installation
- Install Docker
- Install NPM
- Clone this repository
- In the root of the repository, run
  ```docker compose build```
## Running the backend
- Got to the root directory
- Run ```docker compose up -d ```
- Go to the `frontend/dashboard` directory
- Run ```npm start``` to start the frontend
- To stop, interrupt `npm` and then in root folder, type
  ```docker compose down```

Alternatively, to view the logs, run ```docker compose up``` in its
own terminal.

## Usage
The various parts of the application can be reached as follows.
- To access the database, you can `psql` to `localhost:5432`.
  The default postgres username is "boss", and the password is "example"
- To access the broker, you can browse to `localhost:15672`.
  The login is "guest" and the password is also "guest"
- To access the backend, you can go to `localhost:8080/docs` for Swagger
  or `localhost:8080/redoc` or Redoc. This
  will display a UI with some documentation on the endpoints.
  It's possible to test authentication by using the username 
  "johndoe" and password "secret"

## About some shortcuts used in this project
This project was developed under certain time constraints, and thus
some shortcuts were needed.
- The front end has no proper login / logout mechanism. The implementation
  chosen simply authenticates using the above provided credentials, but
  while a failing login will generate an error in the Javascript, it
  does not actually prevent logging in.
- The backend does no proper authentication. Rather it uses a number of 
  fake methods to simulate the process of logging in. Of course none of
  this would be used in a proper login
- This project is not tested. Bad. It's been prepared for testing in the
  sense that it's possible to specify different database parameters etc,
  but no tests were implemented.
- The sensor is tightly coupled to the backend. It would probably be
  better to have the sensor publish to the message queue, then read that
  message queue from the backend.
- The backend code structure is not very clear, and could be improved.
  The current setup is:
  - main -> sets up the backend, and defined the endpoints
  - setup_alchemy -> sets up the orm for PG access
  - setup_fastapi -> configures FastAPI
  - orm_models -> contains all the SQLAlchemy models for database operations
  - serializers -> contains the Pydantic models for validating endpoint data
  - sensor -> implementation of reading / writing sensor data
  - login -> handles authentication functionality
- Concurrency is not implemented well. For example, writing the
  sensor data to the database is done in a loop. If one of the 
  writes fail, the loop is aborted and causes all the writes to be
  canceled. Better would be to create tasks, then wait for the result
  so writes do not break each other.
- The frontend does not look very nice, and is more a proof of concept than
  what a dashboard should look like.
- Regarding the graph, I wasn't sure what was meant by "summed timeseries with standard 5",
  so I rendered all timeseries in separate graphs. Adding them up would
  also be possible, then I would have probably grouped them in the backend.

## Improvements that could be made
- All the usernames and passwords are hardcoded in the source. That is 
  of course unacceptable, and should be handled through Docker Secrets
- Tests. Of course.
- Resilience. There are various points of possible failure. For example
  if the database is down, the POST endpoint for sensor data will now simply
  error out. Depending on the criticalness of this information, better patterns
  exist for ensuring the data is recorded
- Read endpoint could be refactored. Most of the data formatting is now
  done in the frontend, such as grouping by machine. This could be done in
  the backend, for performance reasons.
- The various Docker containers generate quite a few warnings.
  These are probably due to version issues, or obsolete settings enabled
  by default. It would be good to examine these and address them. However,
  they don't interfere with execution of the backend.