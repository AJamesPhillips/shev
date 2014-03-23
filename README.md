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
    $ cd shev
    shev$ python manage.py syncdb
    python manage.py loaddata roster/sample/shift_type.json roster/sample/team_or_agency.json roster/sample/outcome.json roster/sample/person.json roster/sample/day.json roster/sample/shift.json

### Start the dev server

    shev$ python manage.py runserver


## Provisioning and deployment

### Provisioning

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab setup
    $ honcho run -e conf/stage.env fab restart:define=t

### Deploying

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab deploy
