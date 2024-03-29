Introduction
============

**autoRobot** presents a collection of extensions and a set of high-level
functions that can be used to automate Robot Structural Analyis (RSA) through
its API.

RSA presents a COM interface written for the .Net environment. This API can be
accessed through `Python.Net <https://github.com/pythonnet/pythonnet>`_ module.
As opposed to IronPyhton, Python.Net is based on pure CPython and doesn't
compromise access to scientific librairies like
`Numpy <https://github.com/numpy/numpy>`_ and
`scipy <https://github.com/scipy/scipy>`_.

Scripts written to automate RSA can look austere when written directly with
the API and the information they contain can be lost in a flurry of
all-capital-twenty-letter words. **autoRobot** provides convenience functions
to shorten the syntax and adds functionalities to the software's internal
servers. Taking advantage of CPython means that the code can be written
in the form of `jupyter notebooks <https://github.com/jupyter/notebook>`_
that offer a convenient interface for short code cells, diagrams and
formatted text.

**autoRobot** can be used for pre- and post-processing tasks.


Installation
------------

.. code-block::

   mkdir autorobot
   git clone https://github.com/jagaudin/autorobot


Usage
-----

**autoRobot** aims at simplifying RSA automation scripts. To use it, just
import ``autorobot`` and initialize the module. ::

    import autorobot as ar
    rb = ar.initialize()


In order to focus on the model's data rather than the syntax, a layer of
high-level methods is provided on top of the original functions.
Some .Net objects are also encapsulated to provide additional functionality
whilst maintaining access to all the original methods and attributes.

For example, the following code is valid:  ::

    import autorobot as ar
    rb = ar.initialize()
    rb.new(ar.RProjType.SHELL)
    n = rb.nodes.create(2., 0., 0.)  # This returns an ExtendedNode instance
    assert(n.X == 2.)  # ExtendedNode instance gives access to IRobotNodes fields and methods

This is to say that the ``X`` attribute of the encapsulated ``IRobotNode``
object is available through the :py:class:`.ExtendedNode` instance.
