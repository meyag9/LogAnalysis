#! /usr/bin/env python
import psycopg2
from datetime import datetime

DBNAME = "news"


def get_query_results(query):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result

"""Which articles have been accessed the most?
Present this information as a sorted list with the
most popular article at the top."""


def topThree():
    query = ("SELECT articles.title, count(*) as views "
             "from articles join log on "
             "articles.slug=SUBSTRING(path FROM 10) "
             "where path != '/' group by SUBSTRING(path FROM 10), "
             "articles.title order by views desc limit 3;")
    results = get_query_results(query)
    return results


'''Who are the most popular article authors of all time? That is,
 when you sum up all of the articles each author has written,
 which authors get the most page views? Present
 this as a sorted list with the most popular author at the top.'''


def topAuthors():
    query = ("SELECT authors.name, count(log.path) "
             "AS views FROM authors LEFT JOIN articles on "
             "authors.id=articles.author LEFT JOIN log ON "
             "articles.slug=SUBSTRING(path FROM 10) "
             "GROUP BY authors.name ORDER BY views DESC;")
    results = get_query_results(query)
    return results


# On which days did more than 1% of requests lead to errors?
# Reference:
# https://discussions.udacity.com/t/logs-analysis-project-query-3/249639
def errorPercent():
    query = ("SELECT date, round(calculated::decimal, 2) "
             "FROM(SELECT date, cast(num_errrors AS FLOAT)"
             "/cast(total AS FLOAT)*100 as calculated FROM calc) "
             "sub WHERE calculated > 1.0;")
    results = get_query_results(query)
    return results


if __name__ == "__main__":
    print "The most popular three articles of all time are: "
    one = topThree()
    count = 1
    for item in one:
        s = "{}. \"{}\" -{} views".format(count, item[0], item[1])
        print s
        count += 1

    print "\nThe most popular article authors of all time are:"
    two = topAuthors()
    count = 1
    for item in two:
        s = "{}. {} -{} views".format(count, item[0], item[1])
        print s
        count += 1

    print "\nMore than 1%" + " of errors occurred on: "
    three = errorPercent()
    fmt = "%B %d, %Y"
    for item in three:
        calc = str(item[1])
        mydate = datetime.strftime(item[0], fmt)
        s = "{} -{}{} errors".format(mydate, calc, "%")
        print s
