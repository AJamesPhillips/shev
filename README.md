shev
====

Project Shev

Scheduling for Hospital Shifts


## Developing

### Setup

We'd recommend using something like virtualenv to manage your packages.

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ honcho run ./manage.py syncdb
    $ honcho run ./manage.py migrate
    $ python manage.py loaddata shev/roster/sample/shift_type.json shev/roster/sample/team_or_agency.json shev/roster/sample/outcome.json shev/roster/sample/person.json shev/roster/sample/day.json shev/roster/sample/shift.json

### Start the dev server

    $ honcho start

### Schema changes and Migrations

Change your models, then:

    $ honcho run ./manage.py schemamigration roster --auto   # generate new migration
    $ honcho run ./manage.py migrate                         # apply the new migration


## Provisioning and deployment

### Provisioning

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab setup

### Deploying

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab deploy:redefine=t

Note the `define=t` will cause nginx and upstart jobs to be rewritten so will need root access
