from random import randint
from time import time, sleep

import logging


class RateControl(object):
    def __init__(self, timeFrame, rateLimit, lookAheadRatio=.1):
        if timeFrame <= 0 or rateLimit <= 0:
            raise ValueError('timeFrame and rateLimit are expected to be positive')
        if lookAheadRatio > .5 or lookAheadRatio < .1:
            raise ValueError('lookAheadRatio should be within .1 and .5`')
        self.timeFrame = timeFrame
        self.rateLimit = rateLimit
        self.lookAheadRatio = lookAheadRatio
        self.lookAheadItems = int(lookAheadRatio * rateLimit)
        base = time()
        # self.timestamps = [base - i*self.step for i in range(0,rateLimit)]
        self.timestamps = [base - timeFrame - 1 for i in range(0, rateLimit)]
        self.indexNow = 0
        self.slowStep = float(timeFrame) / rateLimit / lookAheadRatio * 2
        # self.slowStep = float(timeFrame) / rateLimit
        logging.info('Slowing delay is {:.1f} seconds'.format(self.slowStep))
        self.slowFactor = self.slowStep

    def inLimit(self):
        timeNow = time()

        indexLookAhead = (self.indexNow + self.lookAheadItems) % self.rateLimit
        timeLookAhead = self.timestamps[indexLookAhead]
        deltaLookAhead = int(timeNow - timeLookAhead)

        if deltaLookAhead < self.timeFrame:
            logging.warn('Limit is coming, slowing with {:.1f} seconds'.format(self.slowFactor))
            self.slowFactor += self.slowStep * (1 - self.lookAheadRatio) * .7
            # self.slowFactor += self.slowStep * .1
            # sleep(self.slowFactor)
            sleep(self.slowStep)
        else:
            if self.slowFactor > self.slowStep:
                # self.slowFactor -= self.slowStep * (1 - self.lookAheadRatio) *.7
                self.slowFactor -= self.slowStep * .1

            if self.slowFactor < self.slowStep:
                self.slowFactor = self.slowStep

        indexNext = (self.indexNow + 1) % self.rateLimit
        timeLast = self.timestamps[indexNext]
        deltaNext = int(time() - timeLast)

        if deltaNext < self.timeFrame:
            delay = self.timeFrame - deltaNext
            logging.info('Have to delay {} seconds'.format(delay))
            sleep(delay)

        self.timestamps[self.indexNow] = time()
        self.indexNow = indexNext
        return True

if __name__ == '__main__':
    rc = RateControl(timeFrame=60, rateLimit=50, lookAheadRatio=.4)
    # print rc.timestamps
    t_start = time()
    for k in range(1, 101):
        if rc.inLimit():
            logging.info(k)
            sleep(.5 * randint(0, 1))
    t_stop = time()
    print t_stop - t_start
    # print rc.timestamps
