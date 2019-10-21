

Deployment Instructions
-----------------------

docker-compose up should do it.
The API should be listening on port 1079.

Solution Overview
-----------------

  - Application : Flask + Gunicorn behind Nginx
  - Caching :     Redis
  - Persistence : postgres via SQLAlchemy

Postgres is included in the container and some data is dumped into it at
compile time. For proper persistence, this should be redirected to a better
postgres deployment that is non-volatile across docker deployments. That can 
be done by providing the following environment variables :

  - `DATABASE_HOST`
  - `DATABASE_PORT`
  - `DATABASE_USER`
  - `DATABASE_PASS`
  - `DATABASE_DB`

Redis is included in the container and should be fine. If you want to use 
something else, the following environment variables are available :

  - `CACHE_REDIS_HOST`
  - `CACHE_REDIS_PORT`
  - `CACHE_REDIS_PASSWORD`

API Endpoints
-------------

Endpoints for list of all something. These probably should be paginated
instead.

  - `/cases` : List all Cases 
  - `/persons` : List of all Persons
  - `/attorneys` : List of all Attorneys 

Endpoints to get a specific item by ID: 

  - `/cases/<id>` : Get a specific Case by ID 
  - `/persons/<id>` : Get a specific Person by ID
  - `/attorneys/<id>` : Get a specific Attorney by ID 


About the Models
----------------

The model used is slightly different from the schema provided, and does not
do all the things the schema requires. The following are the additional 
assumptions made :

  - Persons are assumed to exist beyond the scope of a Case, ie, a Person can 
    be involved in multiple Cases.
  - A Person can therefore be represented by multiple Attorneys in the context
    of multiple Cases.
  - A Person involved in a Case can have multiple Attorneys. 
  - Different people on the same side of a Case can have different Attorneys.
  - Attorneys are assumed to be Persons.
  - Attorneys are assumed to be in the bar of only a single state.
  
There remain the following potential issues that should ideally be fixed :

  - "A person cannot be plaintiff and defendant on the same case" is not 
    addressed. At all. It is currently assumed whatever code puts the data 
    into the database will do some kind of validation. I'm sure a way to 
    work in this constraint exists, but I don't know what it is right now.
  - The models don't handle delete well at all. Specifically, cascade delete 
    is not set for the models, and should. The current code will leave 
    dangling CaseParties, PersonAssociations, and AttorneyAssociations if
    the database even allows the delete to begin with. That would also be 
    something that I'd want to address only with greater context of the use 
    case, and specifically, what happens to the persons and attorneys when 
    a case goes away.

Both these issues are likely due to an unasked for generalization of schema, 
or more specifically, you likely asked for something else entirely.     

Additional Notes
----------------

  - None of the solution is meaningfully documented.
  - There's no CI/CD implemented on this.
  