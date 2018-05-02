Project: Log Analysis
=====================
## Description
This project is to create a reporting tool that prints out reports (`example.txt`) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

## Instruction of install virtual machine
* You can download and unzip the file: [FSND-Vrtual-Machine](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) or fork and clone the repository (https://github.com/udacity/fullstack-nanodegree-vm).
* In the terminal, `cd` to this new directory and there is a folder named **vagrant**. Change the directory to **vagrant**, run the command `vagrant up` to start the virtual machine.
* When `vagrant up` is finished running, you can run `vagrant ssh` to log in the VM

## Instruction of running report_tool.py
* Download the file: [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip the file after downloading it. The file inside is named `newsdata.sql` and put it into the file `vagrant`.
* Download the `log-analysis-project` folder and put it into the `vagrant` directory.
* Change the directory to `/vagrant`.
* To load the data, run the command `psql -d news -f newsdata.sql`
* `cd` into the `log-analysis-project` directory.
* enter `python report_tool.py ` in terminal.

## The SQL queries for each question.
1. What are the most popular three articles of all time?
```
select A.title, count(*) as views
from articles as A, log as L
where L.path = concat('/article/',A.slug)
group by title
order by views desc
limit 3
```
2. Who are the most popular article authors of all time?
```
select A.name, count(*) as views from
(select title, slug, name
    from articles, authors
    where articles.author = authors.id) as A,
log as L
where L.path = concat('/article/', A.slug)
group by A.name
order by views desc;
```
3. On which days did more than 1% of requests lead to errors?
```
select F.date,
(round(F.error_status::numeric/F.total_status::numeric*100,1)) as error_percentage from
(select E.date, E.error_status, T.total_status from
  (select to_char(time, 'Mon DD, YYYY') as date, count(status) as error_status
    from log
    where status = '404 NOT FOUND'
    group by date) as E,
  (select to_char(time, 'Mon DD, YYYY') as date, count(status) as total_status
    from log
    group by date) as T
  where E.date = T.date) as F
where round(F.error_status::numeric/F.total_status::numeric*100,1) > 1
order by error_percentage desc
limit 1;
```
