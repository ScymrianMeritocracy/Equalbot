#!/usr/bin/python

import os
import praw
import time
import yaml

def countposts(posts, conf):
    """Return submissions over our limit."""
    naughty = []
    for user in posts:
        while len(posts[user]) > conf["count"]:
            naughty.append(posts[user].pop(0))
    return naughty

def getposts(rsub, conf):
    """Fetch all submissions posted within our timeframe."""
    myposts = []
    mynow = int(time.time())
    seconds = conf["hours"] * 60 * 60
    allposts = rsub.get_new(limit = 0)
    for post in allposts:
        if (mynow - post.created_utc) > seconds:
            break
        else:
            myposts.append(post)
    return myposts

def sortposts(posts):
    """Sort submissions by user."""
    counts = {}
    for post in posts:
        if counts.has_key(post.author.name):
            counts[post.author.name].append(post.id)
        else:
            counts[post.author.name] = [post.id]
    return counts

def remove(posts, r):
    """Remove list of submissions."""
    for post in posts:
        r.get_submission(submission_id = post).remove()

def warn(posts, r, conf):
    """Post comments explaining why we removed the submission."""
    for post in posts:
        mypost = r.get_submission(submission_id = post)
        comment = mypost.add_comment(conf["comment"])
        comment.distinguish()

if __name__ == "__main__":
    # load configuration options from file beside ourself
    mypath = os.path.dirname(os.path.realpath(__file__))
    myconf = open(mypath + "/equalconf.yaml", "r")
    conf = yaml.safe_load(myconf)
    myconf.close()

    # connect to reddit
    r = praw.Reddit(user_agent=conf["useragent"])
    r.config.decode_html_entities = True
    r.login(username=conf["username"], password=conf["password"])

    # check and change our list of subreddits
    for sub in conf["subs"]:
        rsub = r.get_subreddit(sub)
        submissions = getposts(rsub, conf)
        userposts = sortposts(submissions)
        violations = countposts(userposts, conf)
        remove(violations, r)
        warn(violations, r, conf)
