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

## Braintree

When testing the cart and checkout in Ch. 8, you can use this test Visa credit card:

    4111 1111 1111 1111
    CVV: 123
    Expiry: 12/24

    More test cards at t.ly/camP

Login to braintree to see your test transactions:

    https://sandbox.braintreegateway.com/login

## Problems

### Unable to load celery application ...

I got this error when I tried to start Celery in the "Testing payments" chapter:

    Error:
    Unable to load celery application
    Module 'myshop' has no attribute 'celery'

The cause was that I was running the command from the parent directory 'myfiles'.
I needed to be in the 'myshop' subdirectory.