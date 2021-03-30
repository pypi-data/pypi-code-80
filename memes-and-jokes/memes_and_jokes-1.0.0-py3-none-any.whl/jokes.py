import praw 
import random


def text(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_text = rand_sub.selftext
    return sub_text

def url(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_url = rand_sub.url
    return sub_url

def title(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_title = rand_sub.title
    return sub_title

def upvotes(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_upvotes = rand_sub.score
    return sub_upvotes

def permalink(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_permalink = rand_sub.permalink
    return sub_permalink

def upvotes_ratio(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_upvotes_ratio = rand_sub.upvote_ratio
    return sub_upvotes_ratio

def author(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_author = rand_sub.author
    return sub_author

def comments(joke_resuts : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("jokes")
    top = subreddit.top(limit = joke_resuts)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_numofcomments = rand_sub.num_comments
    return sub_numofcomments