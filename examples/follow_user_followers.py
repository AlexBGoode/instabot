"""
    instabot example

    Workflow:
        Follow user's followers by username.
"""

import sys
import os
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()

bot = Bot(
    max_likes_per_day=10000,
    max_unlikes_per_day=1000,
    max_follows_per_day=35000,              # 350
    max_unfollows_per_day=350,
    max_comments_per_day=0,
    max_likes_to_like=100,
    filter_users=True,
    max_followers_to_follow=19000,
    min_followers_to_follow=0,              # 10 default
    max_following_to_follow=10000,
    min_following_to_follow=10,
    max_followers_to_following_ratio=10,
    max_following_to_followers_ratio=10000, # 2 default
    max_following_to_block=2000,
    min_media_count_to_follow=0,            # 3 default
    like_delay=60,
    unlike_delay=60,
    follow_delay=60,
    unfollow_delay=60,
    comment_delay=60,
    whitelist=False,
    blacklist="black-whitelist/blacklist.txt",
    comments_file=False,
    stop_words=['shop', 'store', 'free', 'smm']
)
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

for username in args.users:
    bot.follow_followers(username)
