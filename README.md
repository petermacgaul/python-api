# Python FastAPI - API

## Config

Configure the environment for the database in the .env.example file

```bash
cp .env.example .env
```

## Run local

### Initialize container

To initialize the containers you can execute the bash script that runs the Docker Compose file, which will start up the API on the port specified in the environment and bring up two MySQL databases (one for scanning and another for saving data), you can use the following command:

```bash
./scripts/create.sh
```

This will create the container and run the migrations. The migrations are run automatically when the container is created.


The data of the databases will be storage in the `app/volumes` folder.

The scanned database is populated with the data from the file `init.sql`.
This script creates a database `testdb` with two tables `users` and `users_ips`.

The ports set in the environment are configured to not have a conflict with the same port on the host.
However, both databases are set to use port `3306`, which is the default for MySQL.

### Stop container

To stop the container, you can run the following command:

```bash
  docker compose down -v
``` 

### Server

Open the browser and go to http://0.0.0.0:5000 or the port set in the environment.


### Access the container

To enter the container, run the following command:

```bash
docker exec -it <container_name> bash
```

Once inside, you can run the tests.

### Run the tests

Inside the container, to run the tests, run the following command:

```bash
./script/tests.sh
```


## API

The documentation for the endpoints is located at the route `/docs` which allows you to see the available endpoints and test them. 
An endpoint is provided to create a user and another to login.

## Solution
When a new database is created, it will verify if connecting to the database is possible. If the connection is successful, all the information in the database will be saved encrypted using HS256.

When the user wants to scan the database, the saved data it will be decrypted, and the system will check if it can connect. If the connection is successful, it will scan all the tables, columns, and one row from each table. 

The scanner has multiple scanners, to add a new one you need to create a new class that inherits from the `Scanner` class and implement the `scan` methods. The scanner will verify if the column name matches the regex or what decides if correspond that type, and if matches, it will set the respective type.

The database information will be saved in the database as a JSON format (I don't prefer this, but it simplifies the problem, although I could use MongoDB) and will create a scan history.

The last scan is shown in the API when the user wants to see the information.

Logs are implemented.
Auth is implemented.

### Example

`POST localhost:5000/database`


```json
{
  "host": "scan-fastapi-db", // The name of the database container
  "port": 3306,
  "username": "peter",
  "password": "password"
}
```


## Feature added
The new feature analyzes a sample of each table and tags it as a compromised sample if the scanner detects raw data instead of encrypted data. This will specifically apply to ip_address and credit_card_number columns.


## Improvements

- Use MongoDB to save the data in a more structured way.
- The API container do not wait to start the database container, it should wait until the database is ready. (This happens on the first time when the DB are being created)
