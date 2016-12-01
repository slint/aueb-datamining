from .twitter import Twitter
from .models import session, Tweet, Category
from sqlalchemy.exc import IntegrityError


def harvest(hashtags, mentions, since_date, place):
    t = Twitter()
    q = (t.query()
         .hashtags(hashtags)
         .mentions(mentions)
         .since(since_date)
         .place(place))
    results = q.execute()
    # Get already existing tweets by twitter_id
    existing = set(session.query(Tweet.twitter_id).all())
    # FIXME: Probably split this to smaller insert transactions.
    for r in results:
        with session.begin_nested():
            if r.id in existing:
                # skip it
                print(r.id, r.text)
            # insert in db
            t = Tweet(twitter_id=r.id, text=r.text)
            try:
                session.add(t)
            except IntegrityError as e:
                print('duplicate tweet: ', r.id, r.text)
                continue
        session.commit()


def categorize():
    pass
