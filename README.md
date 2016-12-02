# REPORT 1

This is a project report for **Politically Correct**, a Twitter harvester/categorizer that focuses on Greek political parties (though being flexible to support any kind of context) and the public reception of their
tweet statuses. The project part of the Athens University of Economics and Business and is hosted on GitHub at https://github.com/slint/aueb-datamining.

## Architecture

The application works in 3 stages:

1. **Harvesting:** Using the Python package `tweepy`, the application makes requests to Twitter's REST API, in order to search and collect all the posted tweets that follow a specific set of criteria, like containing hashtags (eg. *#NewDemocracy*), user mentions (eg. *@tsipras*), being created from a specific date or being posted inside a specific location (eg. *Greece, Athens, Germany, etc*).

   The collected tweets are then being stored in an Database which follows a simple schema/model, generated and maintained using that Python's `SQLAlchemy` package. BecauseSQLite this database model is described through Python objects, it easy to run all of these examples in any database supported by SQLAlchemy, from *SQLite* to *PostgreSQL* and *MySQL*.   

   The database model consists of two simple entities, the **Tweet** and the **Category** that share a many-to-many relationship. This means that a *Tweet* can belong in multiple *Categories* and that a single *Category* may be assigned to more than one *Tweet*. We try to hold the minimum amount of data for our purposes, so we only store the `id` and `text` of a Tweet. For Categories we have a short tag and long description.  

2. **Categorizing:** The next part of the process is categorization, which takes place on a set of collected Tweets from the previous step. We go through all of the tweets trying to categorize them based on the contents of their message.

   Two categories interest us at the moment, **positive** and **negative**. Positive tweets contain "positive" emoticons, like smiley faces ( `:)`, `:D` ) and hearts ( `<3` ). *Negative* tweets are the ones that contain "negative" emoticons, like frowny faces ( `:(` ), crying ( `:'(` ) or broken hearts ( `</3`). For each tweet we search for the relevant emoticon inside its text and if found, we add the tweet to the `positive` or `negative` Categories. 

3. **Reporting:** The reporting process is as simple as querying over the database to basicly produce counts for the two categories, so a simple query. 


All of these steps (and additional utilites) are being called from a CLI implemented using the Python library `click`. 

## Technologies

Python (`v3.5` but probably still fine with `v2.7`) served as the main programming language to design and implement the project, although in the background automatically generated SQL queries perform the database transactions. The main library/package highlights that made this project possible are:

- `tweepy`, a Twitter API wrapper (https://github.com/tweepy/tweepy)
- `SQLAlchemy`, an Object Relational Mapping library (https://bitbucket.org/zzzeek/sqlalchemy)
- `click`, a CLI design library (https://github.com/pallets/click)

## Strategy - Usage

To use this library one has to follow these simple steps from his CLI:

1. (Optional but recommended: create a Python virtualenv.)
2. Clone the GitHub repository, and `cd` inside of it.
3. Run `pip install -r requirements.txt` to install the project's dependencies.
4. Run `python cli.py --help` to check out the available options.
5. Check the `config.py` for the available configuration variables (mainly Twitter API credentials). One can set these either directly inside the `config.py`, or by exporting them to their environment (eg. `export TWITTER_API_TOKEN=secret-token-123`)
6. Run `python cli.py db create` to create an instance of the application's database (you have to define the connection string through the `DATABASE_URL` configuration variable).
7. Run `python cli.py harvest -h NewDemocracy -h ND -m kmitsotakis -s 2016-11-15 -p Greece` to start  harvesting Twitter's API.
8.  

## Results

Results are given as two `CSV` files, `negative.csv` and `positive.csv`, containing the Tweet's ID and text.