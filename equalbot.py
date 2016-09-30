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
        if post.author.name in counts.keys():
            counts[post.author.name].append(post.id)
        else:
            counts[post.author.name] = [post.id]
    return counts

def remoteconf(sub):
    """Return parsed remote config for a subreddit."""
    try:
        page = r.get_wiki_page(sub, "equalbot")
        rconf = yaml.safe_load(page.content_md)
    except:
        print(sub + ": trouble parsing wiki page")
        return None
    if "count" in rconf and "hours" in rconf:
        return rconf

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
    # load subreddit list from file beside ourself
    mypath = os.path.dirname(os.path.realpath(__file__))
    myconf = open(mypath + "/sublist.yaml", "r")
    conf = yaml.safe_load(myconf)
    myconf.close()

    # connect to reddit
    r = praw.Reddit()

    # check and change our list of subreddits
    for sub in conf["subs"]:
        rconf = remoteconf(sub)
        if not rconf:
            continue
        rsub = r.get_subreddit(sub)
        submissions = getposts(rsub, rconf)
        userposts = sortposts(submissions)
        violations = countposts(userposts, rconf)
        remove(violations, r)
        if "comment" in rconf:
            warn(violations, r, rconf)
