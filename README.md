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
    $ python manage.py loaddata shev/roster/sample/shift_type.json shev/roster/sample/team_or_agency.json shev/roster/sample/outcome.json shev/roster/sample/person.json shev/roster/sample/day.json shev/roster/sample/shift.json

### Start the dev server

    shev$ python manage.py runserver


## Provisioning and deployment

### Provisioning

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab setup
    $ honcho run -e conf/stage.env fab restart:redefine=t

### Deploying

    $ virtualenv venv
    $ source venv/bin/activate
    $ honcho run -e conf/stage.env fab deploy
