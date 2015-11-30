=============================
django-pj-portfolio
=============================

.. image:: https://badge.fury.io/py/django-pj-portfolio.png
    :target: https://badge.fury.io/py/django-pj-portfolio

.. image:: https://travis-ci.org/jokimies/django-pj-portfolio.png?branch=master
    :target: https://travis-ci.org/jokimies/django-pj-portfolio

.. image:: https://codecov.io/github/jokimies/django-pj-portfolio/coverage.svg?branch=master
    :target: https://codecov.io/github/jokimies/django-pj-portfolio?branch=master


Portfolio tracking

Documentation
-------------

The full documentation is at
https://django-pj-portfolio.readthedocs.org. (at some point) 

Quickstart
----------

Install django-pj-portfolio::

    pip install django-pj-portfolio

Then to use it in a project, add `portfolio` into ``INTALLED_APPS``::

  INSTALLED_APPS = (
  ....
  'portfolio',
  )

And apply the migrations::

  python manage.py migrate


Configure `urls`, add to main `urls.py`::
  
  ...
  url(r'^portfolio/', include('portfolio.urls')),
  ...


Update price trackers (for updating the prices)::

  python manage update_price_trackers

For daily price tracking, `update_share_prices` can be used::

  python manage update_price_values

Updates prices once per day (even if run multiple times a day, the first
price only is taken in to account)


Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
