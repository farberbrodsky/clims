# clims
An unofficial CLI for ims.tau.ac.il

Required packages:
```pip3 install appdirs lxml bs4 requests```

To list your scans, run:
```
$ python3 main.py scans-list 20201
[{'status': 'הזמנה', 'course': 'אלגברה לינארית 1א'}]
```
Where 20201 means the first semester of 2020.

To fetch any other URL (to implement any feature that isn't in here), run:
```
$ python3 main.py fetch /Tal/TP/Tziunim_P.aspx?src=&sys=tal&rightmj=1
```
?id= is added automatically.
