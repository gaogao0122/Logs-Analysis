#!/usr/bin/env python
import psycopg2


def main():
    db = psycopg2.connect("dbname = news")
    cursor = db.cursor()
    # 1. What are the most popular three articles of all time
    cursor.execute("select A.title, count(*) as views " +
                   "from articles as A, log as L " +
                   "where L.path = concat('/article/',A.slug) " +
                   "group by title " +
                   "order by views desc " +
                   "limit 3")
    result = cursor.fetchall()
    print("-----------------------Question 1---------------------------")
    print("1. What are the most popular three articles of all time?\n")
    for tuple in result:
        print (tuple[0] + " -- " + str(tuple[1]) + " views")
    # 2. Who are the most popular article authors of all time?
    cursor.execute("select A.name, count(*) as views from " +
                   "(select title, slug, name from articles, authors " +
                   "where articles.author = authors.id) as A, log as L " +
                   "where L.path = concat('/article/', A.slug) " +
                   "group by A.name order by views desc")
    result = cursor.fetchall()
    print("\n-----------------------Question 2---------------------------")
    print("2. Who are the most popular article authors of all time?\n")
    for tuple in result:
        print (tuple[0] + " -- " + str(tuple[1]) + " views")
    # 3. On which days did more than 1% of requests lead to errors?
    cursor.execute("select F.date, " +
                   "(round(F.error_status::numeric/" +
                   "F.total_status::numeric*100,1)) " +
                   "as error_percentage from " +
                   "(select E.date, E.error_status, T.total_status from " +
                   "(select to_char(time, 'Mon DD, YYYY') as date, " +
                   "count(status) as error_status from log " +
                   "where status = '404 NOT FOUND' group by date) as E, " +
                   "(select to_char(time, 'Mon DD, YYYY') as date, " +
                   "count(status) as total_status from log " +
                   "group by date) as T where E.date = T.date) as F " +
                   "where round(F.error_status::numeric/" +
                   "F.total_status::numeric*100,1) > 1 " +
                   "order by error_percentage desc limit 1")
    result = cursor.fetchall()
    print("\n-----------------------Question 3---------------------------")
    print("3. On which days did more than 1% of requests lead to errors?\n")
    for tuple in result:
        print (tuple[0] + " -- " + str(tuple[1]) + "%")
    db.close()


main()
