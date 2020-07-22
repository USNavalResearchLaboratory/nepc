Accessing a NEPC MySQL database
===============================

You have two options for accessing a NEPC MySQL database of cross
sections via the nepc Python module: 1. the production MySQL server
hosted at NRL (requires NRL network access) 2. a “local” MySQL server
running on “localhost” (presumably the computer you are using right now)

If you are not familiar with SQL and database management, then option 2
is probably not for you, and you should just go with option 1. If you
want/need to pursue option 2, then the following notes may be helpful.
We do assume, however, some basic understanding of MySQL server
installation and management.

“local” NEPC MySQL database installation
----------------------------------------

1. Install MySQL

MySQL Sever 8.0 is recommended, and installation instructions are at
`this link <https://dev.mysql.com/doc/refman/8.0/en/installing.html>`__.
For macOS, we recommend the native installer at `the MySQL Community
Server downloads page <https://dev.mysql.com/downloads/mysql/>`__.

2. Configure MySQL

Once MySQL is installed, you will need to add two user accounts–a
personal account with full read/write access to the ``nepc`` and
``nepc_test`` databases, and a ‘nepc’ account with read-only access to
the NEPC database. Put the following commands in a script named
``nepc_user_script.sql`` (replacing ``MySQL_username`` and
``MySQL_password`` with your username and your password):

.. code:: sql

   CREATE USER 'MySQL_username'@'localhost'
     IDENTIFIED BY 'MySQL_password';
   GRANT ALL 
     ON nepc.*
     TO 'MySQL_username'@'localhost';
   GRANT ALL 
     ON nepc_test.*
     TO 'MySQL_username'@'localhost';

   CREATE USER 'nepc'@'localhost'
     IDENTIFIED BY 'nepc';
   GRANT USAGE ON *.* TO `nepc`@`localhost` 
   GRANT SELECT
     ON nepc.* 
     TO 'nepc'@'localhost';
   GRANT SELECT
     ON nepc_test.* 
     TO 'nepc'@'localhost';

The first block creates the user ``MySQL_username`` and gives them
read/write access to ``nepc`` and ``nepc_test`` databases. The second
block will setup the ``nepc`` user for read access to ``nepc`` and
``nepc_test``. You can run the script with
``mysql -u root -p < nepc_user_script.sql``.

NEPC will need access to your personal MySQL credentials, so you will
need to put them in a file at ``$HOME/.mysql/defaults``:

.. code:: shell

   [client]
   user=MySQL_username
   password=MySQL_password

3. Build the database

The script ``$NEPC_HOME/nepc/mysql/build.py`` will build a NEPC-style
database named ``nepc`` from a properly structured set of data files in
``$NEPC_DATA_HOME``. If the script is run with the ``--test`` argument,
it will build the ``nepc_test`` database using the data in
``$NEPC_HOME/tests/data``.

MySQL performance
-----------------

You may need to `troubleshoot slow MySQL
performance <https://confluence.atlassian.com/kb/troubleshooting-slow-mysql-performance-785453959.html>`__.

There are some MySQL server `configuration variables that may make your
NEPC database run much
faster <http://www.speedemy.com/17-key-mysql-config-file-settings-mysql-5-7-proof/>`__.

First, you need to find out which MySQL options file is read when
starting mysqld (MySQL server) so that you can set the variables:

.. code:: console

   $ /usr/sbin/mysqld --help --verbose --skip-networking --pid-file=$(tempfile) 2> /dev/null | grep -A1 'Default options are read'

You should get an output like this:

.. code:: console

   Default options are read from the following files in the given order:
   /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf 

If that doesn’t work, you can try `some other
approaches <https://www.psce.com/en/blog/2012/04/01/how-to-find-mysql-configuration-file/>`__.

Add the following lines to the appropriate configuration file (e.g. 
``/etc/mysql/mysql.conf.d/mysqld.cnf``)

.. code:: console

   innodb_buffer_pool_size=40000000000
   innodb_log_file_size=2000000000
   innodb_flush_log_at_trx_commit=0
   sync_binlog=0
   innodb_flush_method=O_DIRECT

There are also some `Linux
parameters <https://www.percona.com/blog/2018/07/03/linux-os-tuning-for-mysql-database-performance/>`__
that you should check and consider modifying if you need to improve
database performance on Linux.
