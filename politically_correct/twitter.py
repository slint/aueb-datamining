import logging
import time

import tweepy
from tweepy import Cursor, OAuthHandler

from .config import cfg


class Twitter(object):
    """Twitter wrapper."""

    SLEEP_TIME = (15 * 60 + 5)

    def __init__(self):
        """Initialize Twitter wrapper."""
        auth = OAuthHandler(cfg.TWITTER_CONSUMER_KEY,
                            cfg.TWITTER_CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(cfg.TWITTER_ACCESS_TOKEN,
                              cfg.TWITTER_ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def query(self, query_args=None):
        """Return a new TwitterQuery object.

        :param query_args: List of raw args to pass to the new `TwitterQuery`.
        """
        return TwitterQuery(self, query_args)

    def get_country(self, name):
        """Return a Place ID for a country search.

        :param name: Name of the country.
        """
        places = self.api.geo_search(query=name, granularity='country')
        if places:
            place_id = places[0].id
        else:
            raise Exception(u'Country {} not found.'.format(name))
        return place_id


class TwitterQuery(object):
    """Twitter Query chainable object."""

    def __init__(self, twitter, query_args=None):
        self.twitter = twitter
        self.query_args = query_args or []

    def _format_hashtag(self, hashtag):
        return hashtag if hashtag[0] == '#' else '#' + hashtag

    def _format_mention(self, mention):
        return mention if mention[0] == '@' else '@' + mention

    def _limit_handled(self, cursor):
        """Return a wrapped cursor that sleeps after a Rate Limit Response."""
        # When cursor.next() returns StopIteration, the loop will break.
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                logging.info('Encountered tweepy.RateLimitError, sleeping for '
                             '{} seconds.'.format(self.SLEEP_TIME))
                time.sleep(self.SLEEP_TIME)
                logging.info('Done sleeping, continue results iteration.')

    def execute(self):
        """Executes the query with any applied argument."""
        if not self.query_args:
            raise Exception('Cannot execute query with no arguments.')
        query = ' '.join(self.query_args)
        print(query)
        results = Cursor(self.twitter.api.search, q=query, rpp=100)
        return self._limit_handled(results.items())

    def hashtags(self, hashtags):
        """Add hashtags to the search query.

        :param hashtags: List of hashtags to search for.
        """
        if hashtags:
            normalized_hashtags = [self._format_hashtag(h) for h in hashtags]
            self.query_args.append('({})'
                                   .format(' OR '.join(normalized_hashtags)))
        return self

    def mentions(self, mentions):
        """Add user mentions to the search query.

        :param mentions: List of user mentions to search for.
        """
        if mentions:
            normalized_mentions = [self._format_mention(m) for m in mentions]
            self.query_args.append('({})'
                                   .format(' OR '.join(normalized_mentions)))
        return self

    def since(self, since_dt):
        if since_dt:
            self.query_args.append(u'since:{}'
                                   .format(since_dt.date().isoformat()))
        return self

    def place(self, place):
        if place:
            self.query_args.append(u'place:{}'
                                   .format(self.twitter.get_country(place)))
        return self
