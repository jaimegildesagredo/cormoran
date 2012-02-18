Tutorial
========

.. warning::
   Cormoran is in a very alpha state so its not recomendable to use it in production software.

Installing
----------
You can install the latest estable version from PyPI.

.. code-block:: bash

   $ pip install cormoran

Or if you want to work with the latest development version, you can install it from GitHub.

.. code-block:: bash

   $ pip install git+git://github.com/jaimegildesagredo/cormoran.git

Importing
---------
Import the Cormoran public API.

>>> from cormoran import *

Defining data
-------------
We need to define a new :class:`Persistent` subclass with all the fields we want to persists.

>>> class User(Persistent):
...    __cormoran_name__ = u'users'
...    email = StringField(nullable=False)
...    name = StringField()
...    is_active = BooleanField(default=False)

The :class:`User` class has `email` and `name` string fields and `is_active` boolean field. The :attr:`__cormoran_name__` is an optional attribute to tell Cormoran which is the name of the collection (the SQL table). If not present will be the class name.

Also an `_id` integer primary field has been automatically generated.

>>> User._id
<cormoran.fields.IntegerField object at 0x7f6845fe6350>

Connecting to a SQLite database
-------------------------------
For this tutorial we will use the SQLite backend. To create a database connection we call :func:`connect` with the uri to our database.

>>> sqlite = connect('sqlite:///tests.sqlite')

We can also use a in-memory SQLite database.

>>> sqlite = connect('sqlite:///:memory:')

Next we will create a :class:`Store` object with our sqlite connection.

>>> store = Store(sqlite)

For now Cormoran doesn't create the database structure and we need to create the tables manually, so we will execute the SQL create table statement.

>>> sqlite._connection.execute('CREATE TABLE users (_id integer primary key, email text not null, name text, is_active bool)')

Creating an object
------------------
Now we will create a new :class:`User` called `Mike` with email `mike@example.com`

>>> user = User(name=u'Mike', email=u'mike@example.com')

and save him to the database.

>>> store.add(user)
>>> store.commit()

Then the `_id` field is populated from database.

>>> user._id == 1
True

Updating an object
------------------
We want to activate our new user.

>>> user.is_active = True
>>> store.add(user)
>>> store.commit()

Finding objects
---------------
Now we want to get all users in our system.

>>> for user in store.find(User):
...    print u'%d: %s <%s>' % (user._id, user.name, user.email)
1: Mike <mike@example.com>

We may also want to filter results. For example get only the active users.

>>> list(store.find(User).filter(is_active=True))
[<__main__.User object at 0x7ff85b681210>]
