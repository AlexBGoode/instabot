# -*- coding: utf-8 -*-
"""
    Filter functions for media and user lists.
"""

from . import delay

# filtering medias


def filter_medias(self, media_items, filtration=True, quiet=False):
    if filtration:
        if not quiet:
            self.logger.info("Received %d medias." % len(media_items))
        media_items = _filter_medias_not_liked(media_items)
        if self.max_likes_to_like:
            media_items = _filter_medias_nlikes(
                media_items, self.max_likes_to_like)
        if not quiet:
            self.logger.info("After filtration %d medias left." % len(media_items))
    return _get_media_ids(media_items)


def _filter_medias_not_liked(media_items):
    not_liked_medias = []
    for media in media_items:
        if 'has_liked' in media.keys():
            if not media['has_liked']:
                not_liked_medias.append(media)
    return not_liked_medias


def _filter_medias_nlikes(media_items, max_likes_to_like):
    filtered_medias = []
    for media in media_items:
        if 'like_count' in media.keys():
            if media['like_count'] < max_likes_to_like:
                filtered_medias.append(media)
    return filtered_medias


def _get_media_ids(media_items):
    result = []
    for m in media_items:
        if 'pk' in m.keys():
            result.append(m['pk'])
    return result


def check_media(self, media_id):
    self.mediaInfo(media_id)
    if len(self.filter_medias(self.LastJson["items"])):
        return check_user(self, self.get_media_owner(media_id))
    else:
        return False

# filter users


def stop_words_found(self, user_info):
    text = ''
    if 'biography' in user_info:
        text += user_info['biography'].lower()

    if 'username' in user_info:
        text += user_info['username'].lower()

    if 'full_name' in user_info:
        text += user_info['full_name'].lower()

    for stop_word in self.stop_words:
        s_w = stop_word.decode('utf-8')
        if (text.find(s_w) > 0):
            self.logger.debug("Found a stop word in the user's info: " + text)
            return True

    return False


def filter_users(self, user_id_list):
    return [str(user["pk"]) for user in user_id_list]


def check_user(self, user_id, filter_closed_acc=False):
    if not self.filter_users:
        return True

    delay.small_delay(self)
    user_id = self.convert_to_user_id(user_id)

    if not user_id:
        return False

    if self.whitelist and user_id in self.whitelist:
        self.logger.debug("Check FALSE: whitelist")
        return True

    if self.blacklist and user_id in self.blacklist:
        self.logger.debug("Check FALSE: blacklist")
        return False

    if self.following == []:
        self.following = self.get_user_following(self.user_id)
    if user_id in self.following:
        self.logger.debug("Check FALSE: following already")
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        return False

    if filter_closed_acc and "is_private" in user_info:
        if user_info["is_private"]:
            self.logger.debug("Check FALSE: private - " + user_info["username"] )
            return False

    # if "is_business" in user_info:
    #     if user_info["is_business"]:
    #         self.logger.debug("Check FALSE: business - " + user_info["username"])
    #         return False

    if "is_verified" in user_info:
        if user_info["is_verified"]:
            self.logger.debug("Check FALSE: verified - " + user_info["username"])
            return False

    if "follower_count" in user_info and "following_count" in user_info:
        if user_info["follower_count"] < self.min_followers_to_follow:
            self.logger.debug("Check FALSE: min_followers_to_follow [{0}] - {1}".format(
                user_info["follower_count"],
                user_info["username"]))
            return False

        if user_info["follower_count"] > self.max_followers_to_follow:
            self.logger.debug("Check FALSE: max_followers_to_follow [{0}] - {1}".format(
                user_info["follower_count"],
                user_info["username"]))
            return False

        if user_info["following_count"] < self.min_following_to_follow:
            self.logger.debug("Check FALSE: min_following_to_follow [{0}] - {1}".format(
                user_info["following_count"],
                user_info["username"]))
            return False

        if user_info["following_count"] > self.max_following_to_follow:
            self.logger.debug("Check FALSE: max_following_to_follow [{0}] - {1}".format(
                user_info["following_count"],
                user_info["username"]))
            return False

        try:
            ratio = user_info["follower_count"] / user_info["following_count"]
            if ratio > self.max_followers_to_following_ratio:
                self.logger.debug("Check FALSE: follower/following ratio [{0}/{1}] - {2}".format(
                    user_info["follower_count"],
                    user_info["following_count"],
                    user_info["username"]))
                return False

            ratio = user_info["following_count"] / user_info["follower_count"]
            if ratio > self.max_following_to_followers_ratio:
                self.logger.debug("Check FALSE: following/follower ratio [{0}/{1}] - {2}".format(
                    user_info["following_count"],
                    user_info["follower_count"],
                    user_info["username"]))
                return False

        except ZeroDivisionError:
            self.logger.debug("Check FALSE: hmm... ZeroDivisionError? - {}".format(user_info["username"]))
            return False

    if 'media_count' in user_info:
        if user_info["media_count"] < self.min_media_count_to_follow:
            self.logger.debug("Check FALSE: min_media_count_to_follow [{0}] - {1}".format(
                user_info["media_count"],
                user_info["username"]))
            return False  # bot or inactive user

    if stop_words_found(self, user_info):
        self.logger.debug("Check FALSE: stop words found - " + user_info["username"])
        return False

    self.logger.debug("Check TRUE: all good - " + user_info["username"])
    return True


def check_not_bot(self, user_id):
    delay.small_delay(self)
    """ Filter bot from real users. """
    user_id = self.convert_to_user_id(user_id)
    if not user_id:
        return False
    if self.whitelist and user_id in self.whitelist:
        return True
    if self.blacklist and user_id in self.blacklist:
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        return True  # closed acc

    if "following_count" in user_info:
        if user_info["following_count"] > self.max_following_to_block:
            return False  # massfollower

    if stop_words_found(self, user_info):
        return False

    return True
