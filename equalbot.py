#!/usr/bin/python

import os
import praw
import time
import ruamel.yaml

def countposts(conf, posts):
    """Return submissions over our limit."""
    naughty = []
    for user in posts:
        while len(posts[user]) > conf["count"]:
            naughty.append(posts[user].pop(0))
    return naughty

def getposts(r, sub, conf):
    """Fetch all submissions posted within our timeframe."""
    myposts = []
    mynow = int(time.time())
    seconds = conf["hours"] * 60 * 60
    allposts = r.subreddit(sub).new()
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
        if post.author.name in counts.keys():
            counts[post.author.name].append(post)
        else:
            counts[post.author.name] = [post]
    return counts

def remoteconf(r, sub):
    """Return parsed remote config for a subreddit."""
    try:
        page = r.subreddit(sub).wiki['equalbot']
        rconf = ruamel.yaml.safe_load(page.content_md)
    except:
        print(sub + ": trouble parsing wiki page")
        return None
    if "count" in rconf and "hours" in rconf:
        return rconf

def remove(r, posts):
    """Remove list of submissions."""
    for post in posts:
        post.mod.remove()

def warn(r, conf, posts):
    """Post comments explaining why we removed the submission."""
    for post in posts:
        comment = post.reply(conf["comment"])
        comment.mod.distinguish()

if __name__ == "__main__":
    # load subreddit list from file beside ourself
    mypath = os.path.dirname(os.path.realpath(__file__))
    myconf = open(mypath + "/sublist.yaml", "r")
    conf = ruamel.yaml.safe_load(myconf)
    myconf.close()

    # connect to reddit
    r = praw.Reddit()

    # check and change our list of subreddits
    for sub in conf["subs"]:
        rconf = remoteconf(r, sub)
        if not rconf:
            continue
        submissions = getposts(r, sub, rconf)
        userposts = sortposts(submissions)
        violations = countposts(rconf, userposts)
        remove(r, violations)
        if "comment" in rconf:
            warn(r, rconf, violations)
