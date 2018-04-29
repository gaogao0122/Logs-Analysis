Project: Log Analysis
=====================
## CREATE VIEW COMMAND:
```
create view list as select AR.*, AU.name
from articles as AR, authors as AU
where AR.author = AU.id; //postgresql
```
## Instruction of report_tool.py
* enter `python report_tool.py ` in terminal.
