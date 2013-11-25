![Travis-CI Build Status](https://travis-ci.org/jordan-wright/rapportive.png)

rapportive.py
=============

Python library to automate Rapportive queries.

You can refer to my blog post [here](http://jordan-wright.github.io/blog/2013/10/14/automated-social-engineering-recon-using-rapportive/) for more information.

##Installation
To install rapportive, just run python setup.py install.

##Usage
```
from rapportive import rapportive
profile = rapportive.request('email@domain.com')
```

Results are received as a Profile object, which contains the following attributes:

* profile.name - Name of contact
* profile.memberships - List of tuples of memberships (Linkedin, Facebook, Blogger, etc.)
* profile.jobinfo - Tuple of (position, company)