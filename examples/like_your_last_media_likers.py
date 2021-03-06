"""
    instabot example
    Workflow:
        Like likers of last medias from your timeline feed.
"""

import sys
import os
import time
import random
from tqdm import tqdm
import argparse
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

def like(bot, user_id, nlikes=3):
    bot.like_user(user_id, amount=nlikes)
    return True

def like_media_likers(bot, media, nlikes=3):
    for user in tqdm(bot.get_media_likers(media),
                     disable=not bot.progress_bar,
                     desc="Media likers"):
        like(bot, user, nlikes)
        time.sleep(10 + 20 * random.random())
    return True

def like_your_feed_likers(bot, nlikes=3):
    last_media = bot.get_your_medias()[0]
    return like_media_likers(bot, last_media, nlikes=3)

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
like_your_feed_likers(bot)
