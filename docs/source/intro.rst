Introduction to Jocument
========================

Jocument is a package of utilities to make it easier to write nicely formatted
reports, papers and blog pieces in `Jupyter Notebook`_.

It broadly breaks down into two types of classes.  Firstly there are the classes
to handle footnotes (:py:class:`jocument.Footnotes`), citations (:py:class:`jocument.Citations`), 
and generic labels such as figures, charts and tables (:py:class:`jocument.Labels`). All formatted
output is done via the :py:class:`jocument.Formatter` class which can be subclassed and customised
if the default implementation isn't what you want.  There are also a few utility classes.

Secondly, there are the styling magics which are used to create nice looking title blocks, page headers
and presentation documents.  Used in conjunction with `Rise`_
one can create impressive interactive powerpoint style presentations which actually looks quite
good.  These are also much easier to use where one doesn't have direct access to the jupyter
implementation and therefore can't edit the `custom.css` file.

To use these classes effectively, it is essential to have the `Python Markdown`_
notebook extension installed.

ToDo:
    A lot of stuff in documentation

.. _Jupyter Notebook: https://ipython.org/notebook.html`
.. _Rise: https://rise.readthedocs.io/en/maint-5.5/>`
.. _Python Markdown: https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/python-markdown/readme.html
