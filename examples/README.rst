===============================
Lipisha Payment IPN Examples
===============================

.. image:: https://img.shields.io/pypi/v/lipisha.svg
        :target: https://pypi.python.org/pypi/lipisha


This folder contains examples of IPN callback implementations for Django and Pyramid.
This is for guidance only - it may be adopted and adapted to fit implementation requirements.

Lipisha Payments API (http://developer.lipisha.com/)


USAGE
--------

Examples require setting up of these environment variables for your platform.

* LIPISHA_API_KEY
* LIPISHA_API_SIGNATURE

    export LIPISHA_API_KEY="<YOUR API KEY>"
    export LIPISHA_API_SIGNATURE="<YOUR API SIGNATURE>"


Then, wire the views and set up the configured URL as the as your IPN callback in your Lipisha account or your lipisha sandbox account.

* Lipisha https://lipisha.com
* Sandbox: http://sandbox.lipisha.com

