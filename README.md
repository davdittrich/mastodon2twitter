# mastodon2twitter
Simple python script to crosspost from Mastodon to Twitter

The script posts one Mastodon post to twitter with each call. I run at as a cron job to automate the process.

Long posts will be auto-splitted and posted as a thread on twitter.

The id of the last post is stored in file lasttoot-tw.txt.  

## Note
At the moment only one media attachment for each post is crossposted, it is part of the first tweet if the post is auto-splitted into multiple tweets.

## Dependencies
Mastobdon.py https://github.com/halcy/Mastodon.py  
[tweepy](https://www.tweepy.org/) https://github.com/tweepy/tweepy   
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 

Follow their installation instructions.

For tweepy you will need to create a file config.py with your twitter api credentials. For Mastodon you will create two files, pytooter_clientcred.secret and pytooter_usercred.secret, with your Maston credentials.

## Conact

Find me on Mastodon at https://fediscience.org/@davdittrich
