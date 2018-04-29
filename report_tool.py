import psycopg2

def main():
    db = psycopg2.connect("dbname = news")
    cursor = db.cursor()
    #1. What are the most popular three articles of all time
    cursor.execute("select A.title, L.views from articles as A,"+
    " (select replace(trim('/article/' from path), '-', ' ') as name, count(path) as views from log "+
    "where path != '/' group by path order by views desc limit 3) as L "+
    "where A.title ilike concat('%', L.name, '%') order by L.views desc;")
    result = cursor.fetchall()
    print("-----------------------Question 1---------------------------")
    print("1. What are the most popular three articles of all time?\n")
    for tuple in result:
        print (tuple[0]+" -- "+ str(tuple[1])+" views")
    #2. Who are the most popular article authors of all time?
    cursor.execute("select list.name, sum(L.times) as views from list, "+
    "(select replace(trim('/article/' from path), '-', ' ') as title, count(path) as times from log "+
    "where path != '/' group by path) as L "+
    "where list.title ilike concat('%', L.title, '%') group by list.name "+
    "order by views desc;")
    result = cursor.fetchall()
    print("\n-----------------------Question 2---------------------------")
    print("2. Who are the most popular article authors of all time?\n")
    for tuple in result:
        print (tuple[0]+" -- "+ str(tuple[1])+" views")
    #3. On which days did more than 1% of requests lead to errors?
    cursor.execute("select F.date, (round(F.error_status::numeric/F.total_status::numeric*100,1)) as error_percentage from "+
    "(select E.date, E.error_status, T.total_status from "+
    "(select to_char(time, 'Mon DD, YYYY') as date, count(status) as error_status from log "+
    "where status = '404 NOT FOUND' group by date) as E, "+
    "(select to_char(time, 'Mon DD, YYYY') as date, count(status) as total_status from log "+
    "group by date) as T where E.date = T.date) as F order by error_percentage desc limit 1;")
    result = cursor.fetchall()
    print("\n-----------------------Question 3---------------------------")
    print("On which days did more than 1% of requests lead to errors?\n")
    for tuple in result:
        print (tuple[0]+" -- "+ str(tuple[1])+"%");
    db.close()

main()
