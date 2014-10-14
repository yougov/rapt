===============
Getting Started
===============

It is highly recommended that you configure some default values in
your environment to make rapt easier to use. For example, you can add
the following to your bash profile. ::

  export VELOCIRAPTOR_URL=http://myvr.com
  export VELOCIRAPTOR_USERNAME=eric

You can also pass these values as options to the main command line. ::

  $ rapt --username eric --host http://myvr.com info
  $ rapt -u eric -H http://myvr.com info

The first time you run rapt it will prompt you for a password. The
password will be stored securely in your local keyring for later.

Actions
=======

Rapt allows triggering the different VR actions.

 - swarm
 - build
 - release*

Each action will open a YAML file in the $EDITOR with the necessary
fields. After editing the file as needed, the YAML file will be used
to perform the action. After the action is completed, the event stream
will be tailed, watching for events pertaining to the action. When the
action finishes (or fails) the rapt will exit.

Actions will typically try to intelligently handle stdin. For example,
to swarm multiple processes in a single application you can try using
the `swarms` subcommand to find the swarms you want to use.::

  $ rapt swarms --app-name foo | rapt swarm

You can also use grep to acheive similar results. For example, if you
had a set of apps using "staging" for the config name: ::

  $ rapt swarms  | grep "*-staging-*" | rapt swarm

Each each of these cases you will get a YAML file that contains a
heading for each swarm where each swarm config can be edited.


Queries
=======

Rapt also allows queries for different models. These queries allow
different logical options, but you can also just use grep!


The Event Stream
================

The event stream can be tailed. Any errors will also print the entire
message in the event stream. The format of the event stream is: ::

  $time $title $tags $extra*

The stream can be grepped and to stop the output, just hit C-c.
