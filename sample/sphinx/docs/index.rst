Welcome to Sphinx's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


reStructuredText Primer
=======================

Lists
-----

* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

Literal blocks
--------------

This is a normal text paragraph. The next paragraph is a code sample::

   It is not processed in any way, except
   that the indentation is removed.

   It can span multiple lines.

This is a normal text paragraph again.

Doctest blocks
--------------

>>> 1 + 1
2

Tables
------

=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

Hyperlinks
----------

This is a paragraph that contains `a link`_.

* :ref:`genindex`
* :ref:`search`

.. _a link: https://domain.invalid/

Code Samples
------------

You can use ``backticks`` for showing ``highlighted`` code.

.. code-block:: python

   def my_function(my_arg, my_other_arg):
       """A function just for me.

       :param my_arg: The first of my arguments.
       :param my_other_arg: The second of my arguments.

       :returns: A message (just for me, of course).
       """
