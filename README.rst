Brutemap
========

.. image:: https://brutemap-dev.github.io/_static/brutemap-logo.jpg
   :target: https://brutemap-dev.github.io
   :alt: Brutemap Logo

|Build Status| |Python 2.7| |License|

.. |Build Status| image:: https://travis-ci.org/brutemap-dev/brutemap.svg?branch=master
    :target: https://travis-ci.org/brutemap-dev/brutemap
    :alt: Build Status

.. |Python 2.7| image:: https://img.shields.io/badge/python-2.7-yellow.svg
   :target: https://www.python.org/downloads/
   :alt: Python

.. |License| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://raw.githubusercontent.com/brutemap-dev/brutemap/master/LICENSE
   :alt: License


What is this?
-------------

Brutemap is an open source penetration testing tool that automates testing accounts to the site's login page, based on **Dictionary Attack**. 
With this, you no longer need to search for other *bruteforce* tools and you also no longer need to ask **CMS What is this?** only to find *parameter* forms, because brutemap will do it automatically. 
Brutemap is also equipped with an attack method that makes it easy for you to do *account checking* or test forms with the *SQL injection bypass authentication* technique.


Installation
------------

**Brutemap** uses **selenium** to interact with the website. So, you need to install **Web Driver** for selenium first. See `here <https://www.seleniumhq.org/docs/03_webdriver.jsp>`_. 
If you have installed the ``git`` package, you only need to clone the repository `Git <https://github.com/brutemap-dev/brutemap>`_. Like this:

::

    $ git clone https://github.com/brutemap-dev/brutemap.git

And, install the required modules:

::

    $ pip install -r requirements.txt


Usage
-----

.. image:: https://brutemap-dev.github.io/_static/preview.svg
   :alt: Preview

For basic use:

::

    $ python brutemap.py -t http://www.example.com/admin/login.php -u admin -p abc, root, default

To display a list of available options:

::

    $ python brutemap.py -h

You can find examples of brutemap usage `here <https://asciinema.org/~hijriyan>`_. 
For more information about available options, you can visit the `User's manual <https://github.com/brutemap-dev/brutemap/wiki>`_.

Contributing
------------

Before contributing to this project, please read the [contributing guidelines](https://github.com/brutemap-dev/brutemap/blob/master/CONTRIBUTING.md).


Donate
------
We hope you are happy and we hope you donate!. Please donate today to: https://paypal.me/aprilahijriyan (thanks!)


Links
-----

* Homepage: https://brutemap-dev.github.io
* Download: `.zip <https://github.com/brutemap-dev/brutemap/zipball/master>`_ (latest version) atau `.tar.gz <https://github.com/brutemap-dev/tarball/master>`_ (latest version).
* Issue tracker: https://github.com/brutemap-dev/brutemap/issues
* User's manual: https://github.com/brutemap-dev/brutemap/wiki
