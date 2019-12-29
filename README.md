# README

## Virtual environment

    cd ~/projects/django/django2_by_example
    . venv/bin/activate

## Development server

    cd ~/projects/django/django2_by_example
    python manage.py runserver

## Run apps

    localhost:8000/blog

## Code

[Django-2-by-Example](https://github.com/PacktPublishing/Django-2-by-Example)
[Errata](https://github.com/Django-By-Example-ZH/Django-By-Example-ZH/issues/6)

## Redis

    # Install Redis server
    brew install redis

    # Run
    redis-server /usr/local/etc/redis.conf &

    # Install Python [bindings](https://redis-py.readthedocs.io/
    pip install redis

## Pip requirements

- Django
- django-taggit
- redis

## Images application

When you view the details for an image, e.g.  http://127.0.0.1:8000/images/detail/6/django-and-duke/, the image created by sorl-thumbnail, sorl thumbnail will create an image of the requested size and copy save a copy of that image in a media/cache subdirectory.
