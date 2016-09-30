Equalbot
========

The equalbot is a simple reddit bot for setting a per user submission count limit in a subreddit. If an account goes over, the equalbot removes posts (newest first) until it is back at the limit. A comment can be left on removed posts so the submitter knows why this happened.

Requirements
------------

 * [PRAW4](https://praw.readthedocs.io/en/praw4/index.html)
 * [PyYAML](http://pyyaml.org/)

Setup
-----

Copy the example configurations to a files called `praw.ini` and `sublist.yaml` (which are expected to be in the same directory as the bot), and edit at least the stuff in caps to suit your needs. Note that the `client_id` and `client_secret` values are obtained in your [account preferences](https://github.com/reddit/reddit/wiki/OAuth2-Quick-Start-Example#first-steps). Then create a wiki page at `/r/YOURSUBREDDIT/wiki/equalbot` and define subreddit-specific settings as YAML, just like for AutoModerator.

    count: 5 # number of posts allowed per...
    hours: 20 # this time period
    comment: "This post was over the limit."

If `comment` is excluded, the equalbot will operate silently.

It is recommended that editing of the wiki page be very restricted. Note that the account used must be a moderator with post and wiki privileges in the sub(s) given.

Usage
-----

Run the equalbot from your crontab:

    */5 * * * * /home/me/equalbot/equalbot.py
