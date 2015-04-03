Equalbot
========

The equalbot is a simple reddit bot for setting a per user submission count limit in a subreddit. If an account goes over, the equalbot removes posts (newest first) until it is back at the limit. Then a comment is left on removed posts so the submitter knows why this happened.

Requirements
------------

 * [PRAW](https://praw.readthedocs.org/)
 * [PyYAML](http://pyyaml.org/)

Setup
-----

Copy the example configuration to a file called `equalconf.yaml` (which is expected to be in the same directory as the bot), and edit at least the stuff in caps to suit your needs. The account used must be a moderator with post privileges in the sub(s) given.

Usage
-----

Run the equalbot from your crontab:

    */5 * * * * /home/me/equalbot/equalbot.py
