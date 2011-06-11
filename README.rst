===========
mr.jeffries
===========

mr.jeffries likes to watch. He is all up in your shit and will tell
anyone he can about it.

mr.jeffries is a monitoring tool for Plone. Instead of just logging
events in files on your server or hiding them away in the ZMI,
mr.jeffries can be polled or push events to anything you damn please.

mr.jeffries is named after the total badass in `Rear Window`_.

.. _`Rear Window`: http://www.imdb.com/title/tt0047396/

Usage
=====
mr.jeffries containers monitors. Monitors are made up of listeners and
dispatchers. Your listeners will listen for and optionally filter
events and then push details of them to all the dispatchers.

The currently available listeners are:
 * Error log listener

The currently available dispatchers are:
 * Mail dispatcher
 * JSON/JSONP dispatcher
