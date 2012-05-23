# Cormoran [![Build Status](https://secure.travis-ci.org/jaimegildesagredo/cormoran.png)](http://travis-ci.org/jaimegildesagredo/cormoran)

Cormoran is a fast and lightweight Python persistence framework.
Its main goal is to provide a fast and easy abstraction layer on top of
various database banckends.

# Installation
You can install the latest stable release from PyPI using pip or easy_install as follows

    $ pip install cormoran

Also you can install and use the latest development code from GitHub using pip.

    $ pip install -e git+git://github.com/jaimegildesagredo/cormoran.git

# Usage
This is a simple Cormoran usage example. The commented code comes from
a sample ToDo application using Cormoran. You can get the entire source
code here: https://github.com/jaimegildesagredo/todo

```python
from cormoran import * # Imports the framework

store = Store(connect('sqlite:///:memory:')) # Connects to a in-memory SQLite database

# Defines the model
class Task(Persistent):
    summary = StringField()
    done = BooleanField(default=False)

# Adds a new item and commits
store.add(Task(summary='foo'))
store.commit()
```

# Testing
To run the test suite you need to install some dependencies. For this I
recommend you to use a Python virtualenv.

    $ cd cormoran
    $ virtualenv env
    $ source env/bin/activate
    $ pip install nose pydoubles pyhamcrest

And now you can run the tests using nose.

    $ nosetests

# Source Code
Cormoran source code is hosted on GitHub and released under the GNU GPLv3.

    https://github.com/jaimegildesagredo/cormoran

# Documentaion
You can read the Cormoran documentation at http://jaimegildesagredo.github.com/cormoran/docs
