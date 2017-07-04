from tqdm import tqdm

from . import limits
from . import delay


def follow(self, user_id):
    user_name = user_id
    user_id = self.convert_to_user_id(user_id)
    if not self.check_user(user_id, True):
        return True

    delay.follow_delay(self)
    if super(self.__class__, self).follow(user_id):
        self.total_followed += 1
        self.logger.info("Followed - {}, in total {}".format(user_name, self.total_followed))
        return True
    else:
        self.logger.error("Not followed - " + user_name)
        return False


    # if limits.check_if_bot_can_follow(self):
    # else:
    #     self.logger.info("Out of follows for today.")
    # return False


def follow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to follow %d users." % len(user_ids))
    for user_id in tqdm(user_ids, disable = not self.progress_bar):
        if not self.follow(user_id):
            # self.logger.error("Not followed user {}".format(user_id))
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user_id):]
            break
    self.logger.info("DONE: Total followed %d users." % self.total_followed)
    return broken_items


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: %s" % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.follow_users(follower_ids[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: %s" % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.follow_users(following_ids[:nfollows])
