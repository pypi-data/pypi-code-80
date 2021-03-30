import praw 
import random


def text(num_of_memes : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = num_of_memes)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_text = rand_sub.selftext
    return sub_text

def url(num_of_memes : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = num_of_memes)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_url = rand_sub.url
    return sub_url

def title(num_of_memes : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = num_of_memes)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_title = rand_sub.title
    return sub_title

def upvotes(num_of_memes : int, username : str, password : str, client_secret : str, client_ID : str):
    reddit = praw.Reddit(client_id = client_ID,
                        client_secret = client_secret,
                        username = username,
                        password = password,
                        user_agent = "pythonpraw")

    subreddit = reddit.subreddit("memes")
    top = subreddit.top(limit = num_of_memes)
    all_submissions = []

    for submission in top:
        all_submissions.append(submission)

    rand_sub = random.choice(all_submissions)
    sub_upvotes = rand_sub.score
    return sub_upvotes