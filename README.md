# README

## WARNING

I didn't get all the features in the bookmarks project working but the modules do contain my notes on how things work.

If you want to see a working solution, go to the solution folder ~/projects/django/django2_by_example_solution/bookmarks_final..  I worked through the features there via my browser to check that everything works.

## Virtual environment

    cd ~/projects/django/django2_by_example
    workon django2_by_example

## Development server

    cd ~/projects/django/django2_by_example
    python manage.py runserver

## Run apps

    localhost:8000/blog
    localhost:8000/account

## Code

[Django-2-by-Example](https://github.com/PacktPublishing/Django-2-by-Example)
[Errata](https://github.com/Django-By-Example-ZH/Django-By-Example-ZH/issues/6)

## Redis

If you don't start the Redis server, you'll see this error:

    redis.exceptions.ConnectionError: Error 61 connecting to localhost:6379.  Connection refused.

### Install Redis server

    brew install redis

### Run

    redis-server /usr/local/etc/redis.conf &

### Install Python [bindings](https://redis-py.readthedocs.io/

    pip install redis

## Pip requirements

See requirements-to-freeze.txt.

## Images application

When you view the details for an image, e.g.  http://127.0.0.1:8000/images/detail/6/django-and-duke/, the image created by sorl-thumbnail, sorl thumbnail will create an image of the requested size and copy save a copy of that image in a media/cache subdirectory.
