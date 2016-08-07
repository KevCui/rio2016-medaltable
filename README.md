---
title: Rio2016MedalTable
description: show Rio2016 Olympic Medal Table in terminal
author: KrazyCevin
tags: CLI, python, script
created:  07 Aug 2016
modified: 07 Aug 2016
---

Rio2016MedalTable
=================

### Requirement
* python3
* tabulate
* beautifulsoup4

### Install python package
* pip install -r requirements.txt

### How to use
```
usage: Rio2016MedalTable.py [-h] [-s {Gold,Silver,Bronze,Total}] [-d]
optional arguments:
  -h, --help            show this help message and exit
  -s {Gold,Silver,Bronze,Total}, --sort {Gold,Silver,Bronze,Total}
                        sort results by number of Gold, Silver, Bronze or
                        Total medals. Default: sort by Total
  -d, --debug           active debug log
```

### Example
* Show medal table sorted by **Total** medals: ```./Rio2016MedalTable.py```
* Show medal table sorted by **Gold** medals: ```./Rio2016MedalTable.py -s Gold```

![Alt text](https://github.com/KrazyCavin/Rio2016MedalTable/blob/master/MedalTable_Screenshot.png "Medal Table Screenshot")
