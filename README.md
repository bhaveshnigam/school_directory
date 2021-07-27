# School Directory Task Attempt

To setup the project run

`source setup.sh` from the root of the project directory.

Once the project dependencies have been installed use `python manage.py runserver 0.0.0.0:8000` to run the dev server. Server should be accessible as per the given command value, i.e. on 0.0.0.0:8000 or localhost:8000

To create a admin login, create a login/password combination using,
`python manage.py createsuperuser` this will guide you through the process of setting up the user. This user access credential is necessary for accessing the Bulk import tool.


#### Missing Scope
- Test cases could've been added, but have been deliberitely skipped for the sake of completion of the project in timely manner.
- Use of proper database, as of now it uses sqlite db, which is not really optimal for production use, but is being used for the sake of simplicity.

