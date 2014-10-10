====
rapt
====

..
   .. image:: https://badge.fury.io/py/rapt.png
       :target: http://badge.fury.io/py/rapt

   .. image:: https://travis-ci.org/ionrock/rapt.png?branch=master
	   :target: https://travis-ci.org/ionrock/rapt

   .. image:: https://pypip.in/d/rapt/badge.png
	   :target: https://pypi.python.org/pypi/rapt


A command line tool for Velocirapter_

* Free software: BSD license
..
   * Documentation: https://rapt.readthedocs.org.

Usage
=====

Swarm all the apps containing `foo`: ::

  $ rapt swarms | grep foo | rapt swarm

This will open your `$EDITOR` with a YAML file that looks like: ::

  foo-prod-worker:
    version: 3.4.5
    size: 2
  foo-prod-web:
    version: 3.4.8
    size: 8

You can edit the file, save and close it. Any swarms that have been
updated will be swarmed accordingly.

After swarming the event stream will be printed for the events related
to your swarm(s). It should close when there is a failure or when
things have finished.

You can also add/edit items::

  $ rapt add app

This will open an editor with the appropriate fields for creating your
app. It will also provide a list of available options in the bottom
area for you to copy/paste from.

If you edit the file outside of this environment you can pass it in
via stdin or as an argument ::

  $ cat my_app.yaml | rapt add app   # via stdin
  $ rapt add app my_app.yaml

Generally if a model you are adding has a name it can be used in place
of the the URI and `rapt` will do the right thing to fix it up for
you.

Getting Started
===============

First off start by installing `rapt`. ::

  $ pip install rapt

Then you need to configure the location of Velociraptor and the
username you use to login into VR. ::

  $ export VELOCIRAPTOR_URL=http://deploy.myhost.com
  $ export VELOCIRAPTOR_USERNAME=mike

The first time you use rapt it will save your password in your local
keyring so you don't have to login everytime.


Help
====

Try the `--help` to see how to use rapt.


Features
========

* TODO


.. _Velociraptor: https://bitbucket.org/yougov/velociraptor
