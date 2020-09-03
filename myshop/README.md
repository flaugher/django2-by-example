# README

## Virtual environment

workon django2_by_example

## URLs

[Product catalog](http://127.0.0.1:8000/)

## Packages

See your requirements file.

The shop example, that uses Celery, also requires rabbitmq:

    brew update && brew install rabbitmq

To have it always run when you boot up, do

    brew services start rabbitmq

## Edit translations

You can also use [Poedit](https://poedit.net/) to edit your translation (.po) files.

## Braintree

When testing the cart and checkout in Ch. 8, you can use this test Visa credit card:

    4111 1111 1111 1111
    CVV: 123
    Expiry: 12/24

    More test cards at t.ly/camP

Login to braintree to see your test transactions:

    https://sandbox.braintreegateway.com/login

## Problems

### Couldn't find URL when checking Rosetta

In the section "Translating URL patterns", you're supposed to open ```http://127.0.0.1/en/rosetta```.  But the pattern can't be found unless you first log into the admin application at ```http://127.0.0.1/admin```.  Once you do that you can enter the rosetta URL.

### Unable to load celery application ...

I got this error when I tried to start Celery in the "Testing payments" chapter:

    Error:
    Unable to load celery application
    Module 'myshop' has no attribute 'celery'

The cause was that I was running the command from the parent directory 'myfiles'.
I needed to be in the 'myshop' subdirectory.