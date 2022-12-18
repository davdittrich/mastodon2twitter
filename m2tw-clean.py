#! /usr/bin/env python3

from mastodon import Mastodon
import tweepy
import config  # credentials for twitter
import math
import textwrap
import requests
import bs4 as BeautifulSoup
from datetime import datetime

LANGUAGE = "english"

# credentials for Mastodon
mastodon = Mastodon(
    access_token='pytooter_usercred.secret',
    api_base_url='https://fediscience.org'
)

# Add the user Id you want to get toots
user_id = "109276496085205920"

# getting toots startin with id
since_id = 1109449987640976370

try:
    ltfile = open('lasttoot-tw.txt', "r")
    since_id = ltfile.readline()
    since_id = int(since_id) + 1
    ltfile.close()
except:
    print("File does not exist\n")

cred = mastodon.me()
timeline = mastodon.account_statuses(id=cred.id, only_media=False, pinned=False, exclude_replies=True, exclude_reblogs=False, min_id=since_id, limit=50)

# for toots in timeline:
tweet = list(timeline)[-1]
log_id = tweet.id

# Original author name of boosted toot
org_name = ""

if (tweet.reblog):
    # id = tweet.reblog.id
    tweet = tweet.reblog
    org_name = tweet.account.display_name
    org_sname = tweet.account.acct


soup1 = BeautifulSoup(tweet.content, 'html5lib')
for match in soup1.findAll('span'):
    match.unwrap()
for match in soup1.findAll('a'):
    match.unwrap()
soup1 = BeautifulSoup(str(soup1), 'html5lib')
soup1 = soup1.get_text("\n\n")

message = str(soup1).replace(" ,", ",").replace("  ", " ")
if len(org_name) > 1:
    # message = "via " + org_name + " (" + '\u0040' + org_sname + ")\n" + message
    message = "via " + org_name + ":\n" + message

mediaurl = None
mediadesc = None
try:
    for media in tweet.media_attachments:
        if media['remote_url'] is not None:
            mediaurl = media['remote_url']
        else:
            mediaurl = media['url']
            mediadesc = media['description']
except:
    print("mediaurl error\n")

# Twitter

# New API 2
# client = tweepy.Client(
#    consumer_key=config.consumer_key,
#    consumer_secret=config.consumer_secret,
#    access_token=config.access_token,
#    access_token_secret=config.access_token_secret
# )

# Old API
auth = tweepy.OAuth1UserHandler(
    config.consumer_key,
    config.consumer_secret,
    config.access_token,
    config.access_token_secret
)
api = tweepy.API(auth)

# message
# obtain length of tweet
tweet_length = len(message)

# check length
if tweet_length <= 280:
    tweet_length_limit = 280

elif tweet_length >= 280:
    # divided tweet_length / 280
    # You might consider adjusting this down
    # depending on how you want to format the
    # tweet.
    tweet_length_limit = 273

# determine the number of tweets
tweet_chunk_length = tweet_length_limit
tweet_count = math.ceil(tweet_length / tweet_chunk_length)

# chunk the tweet into individual pieces
tweet_chunks = textwrap.wrap(message,  math.ceil(tweet_chunk_length), break_long_words=False, replace_whitespace=False )

# iterate over the chunks
x = 1
for chunk in (tweet_chunks):
    if x == 1:
        if tweet_count > 1:
            part = ''.join([chunk, " … ", str(x), "/", str(tweet_count)])
        else:
            part = chunk

        if mediaurl:
            r = requests.get(mediaurl)
            f_type = r.headers['Content-Type']
            f_name = path.basename(mediaurl)
            if r.status_code == requests.codes.ok:  # image returned OK
                f = io.BytesIO(r.content)
                response = api.media_upload(filename=f_name, file=f)
                api.create_media_metadata(media_id=response.media_id, alt_text=mediadesc)
                result = api.update_status(status=part, media_ids=[response.media_id])
                f.close()
            else:
                print("error fetching image\n")
            r.close()
        else:
            result = api.update_status(status=part)

    else:
        if x == tweet_count:
            part = ''.join([chunk, " ", str(x), "/", str(tweet_count)])
        else:
            part = ''.join([chunk, " … ", str(x), "/", str(tweet_count)])
    result = api.update_status(status=part, in_reply_to_status_id=tweetid)
    x = x+1
    tweetid = result.id


# Logging
fout = open('mastodon2twitter.log', 'a')
out = ' '.join([datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), " ", str(tweetid), " ", str(tweet.id), "\n"])
fout.write(out)
fout.close()

ltfile = open('lasttoot-tw.txt', 'w')
ltfile.write(str(log_id))
ltfile.close()
