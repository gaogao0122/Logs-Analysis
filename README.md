Project: Log Analysis
=====================
##Instruction of report_tool.py

##CREATE VIEW COMMAND:
```
create view list as select AR.*, AU.name from articles as AR, authors as AU where AR.author = AU.id; //postgresql
```
