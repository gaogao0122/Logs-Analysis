Project: Log Analysis
=====================
## Instruction of running report_tool.py
* Put the `log-analysis-project` folder into the `vagrant` directory.
* `cd` into the `log-analysis-project` directory and use the command `psql -d news -f newsdata.sql` to load the data.
* enter `python report_tool.py ` in terminal.

## The SQL queries for each question.
1. What are the most popular three articles of all time?
```
select A.title, L.views
from articles as A,
(select replace(replace(log.path, '/article/', ''), '-', ' ') as name,
  count(path) as views
  from log
  where path != '/'
  group by path
  order by views desc
  limit 3) as L
where A.title ilike concat('%', L.name, '%')
order by L.views desc;
```
2. Who are the most popular article authors of all time?
```
select A.name, sum(L.views) as times from
(select articles.title, authors.name
  from articles, authors
  where articles.author = authors.id) as A,
(select replace(replace(log.path, '/article/', ''),'-',' ') as title,
  count(log.path) as views
  from log group by path) as L
where A.title ilike concat('%', L.title, '%')
group by A.name
order by times desc;
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
