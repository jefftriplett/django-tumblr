djumblr: Tumblr for Django
==========================

Warning
-------

Currently django-tumblr is under-going some major changes. It may not be stable and I'm not going
to guarantee backwards compatibility until it's ready for a release.


Installation
------------

To install the latest version:

    pip install git+git://github.com/jefftriplett/django-tumblr.git#egg=django-tumblr

``django-tumblr`` has some additional dependencies:

* ``pip install poster``
* ``pip install git+git://github.com/jefftriplett/python-tumblr.git#egg=python-tumblr``
* ``pip install django-taggit``
* ``pip install django-haystack`` -- optional for search integration

Add ``djumblr`` to your project's ``INSTALLED_APPS`` setting.

    INSTALLED_APPS = (
        'djumblr',
        ...
    )

Add ``djumblr`` to your project's ``urls.py``:
    urlpatterns = patterns('',
        (r'^djumblr/', include('djumblr.urls')),
        ...
    )


Instructions
------------

Download djumblr and put it on your pythonpath. Include it in your ``INSTALLED_APPS``, and syncdb.
You now have models for tumblr content!

To sync, you first need to define the user(s) that have tumblr accounts. This is done with the
``TUMBLR_USERS`` settings in settings.py.

An example (from djumblr.scripts.populate_all()):
John has the username ``john`` on his django website, but ``ignorantcarrot`` on tumblr.
His ``TUMBLR_USERS`` would be:

    TUMBLR_USERS = { 'john': 
        { 'tumblr_user': 'ignorantcarrot', }
    }

If he wants to use the django site both for posting and syncing, he would have to 
update the TUMBLR_USERS variable with the email address and password he uses to
log in to tumblr.com:

    TUMBLR_USERS = { 'john': 
        {
            'tumblr_user': 'ignorantcarrot',
            'email': 'john.carrot@fullbladder.net',
            'password': 'secret',
        }
    }

Once installed and configured, you may sync your tumblr accounts with:

    python manage.py sync_tumblr

Alternatively, run ``populate_models(tumblr_user, user)`` from the scripts module, where ``tumblr_user``
is a string containing the username of the tumblr user, and ``user`` is a User object.
