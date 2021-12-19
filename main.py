#Scans subreddits and saves a reference of each new post which matches a particualr flair

import praw
import os

reddit = praw.Reddit('bot1')

#checking for an existing list of posts checked and creating one if none exists.
if not os.path.isfile("posts_checked.txt"):
    posts_checked = {}
else:
    with open("posts_checked.txt", "r", encoding="utf-8") as f:
        posts_checked = {}
        posts_list = f.read()
        posts_list = posts_list.split("\n")
        for item in posts_list:
            try:
                ref = item[:item.index(":")]
                title = item[item.index(":")+2:]
                posts_checked[ref] = title
            except ValueError:
                pass

#Dictionary which holds subreddits as keys, and chosen subreddit flair as values.
#Add any additional search criteria as key/value pairs.
subreddit_ref = {"Cooking": "Recipe to share", "Volumeeating": "Recipe"}

#Scans the new posts for each subreddit, adding any posts it finds with the matching flair to our dictionary
for key in subreddit_ref:
    print("Bot scanning: r/" + key)
    subreddit = reddit.subreddit(key)
    for submission in subreddit.new(limit=50):
        if submission.id not in posts_checked and submission.link_flair_text == subreddit_ref[key]:
            print("Bot scanning new recipe: ", submission.title)
            posts_checked[submission.id] = submission.title
            
#Saves the updated list of posts with matching flair to a txt document.
with open("posts_checked.txt", "w", encoding="utf-8") as f:
    for post in posts_checked:
        f.write(post + ": " + posts_checked[post] + "\n")
