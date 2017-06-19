"""
    Function to calculate delays for like/follow/unfollow etc.
"""

from time import time
from time import sleep
import random



def add_dispersion(delay_value):
    v = delay_value * (1 + random.random() / 5)
    # print v
    return v


def like_delay(bot):
    t = time()
    d = t - bot.like_delay_moment
    if d < bot.like_delay:
        d = bot.like_delay - d
        bot.logger.debug("like_delay: have to wait {:.0f} more seconds".format(d))
        sleep(add_dispersion(d))

    bot.like_delay_moment = time()


def unlike_delay(bot):
    t = time()
    d = t - bot.unlike_delay_moment
    if d < bot.unlike_delay:
        d = bot.unlike_delay - d
        bot.logger.debug("Unlike_delay: have to wait {:.0f} more seconds".format(d))
        sleep(add_dispersion(d))

    bot.unlike_delay_moment = time()


def follow_delay(bot):
    t = time()
    d = t - bot.follow_delay_moment
    if d < bot.follow_delay:
        d = bot.follow_delay - d
        bot.logger.debug("follow_delay: have to wait {:.0f} more seconds".format(d))
        sleep(add_dispersion(d))

    bot.follow_delay_moment = time()

def unfollow_delay(bot):
    t = time()
    d = t - bot.unfollow_delay_moment
    if d < bot.unfollow_delay:
        d = bot.unfollow_delay - d
        bot.logger.debug("unfollow_delay: have to wait {:.0f} more seconds".format(d))
        sleep(add_dispersion(d))

    bot.unfollow_delay_moment = time()


def comment_delay(bot):
    sleep(add_dispersion(bot.comment_delay))


def block_delay(bot):
    sleep(add_dispersion(bot.block_delay))


def unblock_delay(bot):
    sleep(add_dispersion(bot.unblock_delay))


def error_delay(bot):
    sleep(10)


def small_delay(bot):
    sleep(add_dispersion(3))


def very_small_delay(bot):
    sleep(add_dispersion(0.7))
