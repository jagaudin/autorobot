Extensions
==========

In order to focus on the model's data rather than the syntax, a layer of high-level methods is provided on top of the original functions.  Some .Net objects are encapsulated to provide new methods together with all the original methods and attributes.

For example, the following code is valid: the ``X`` attribute of the encapsulated ``IRobotNode`` object is available through the :py:class:`.ExtendedNode` instance. ::

    import autorobot as ar
    rb = ar.initialize()
    rb.new(ar.RProjType.SHELL)
    n = rb.nodes.create(2., 0., 0.)  # This returns an ExtendedNode instance
    assert(n.X == 2.)  # ExtendedNode instance gives access to IRobotNodes fields and methods


.. automodule:: autorobot.extensions

.. _objects:

Objects
-------

.. autoclass:: ExtendedNode
  :members:
  :inherited-members:


.. _application:

Application
-----------

.. autoclass:: ExtendedRobotApp
   :member-order: 'bysource'
   :members:

.. autodata:: app
  :annotation:


.. _servers:

Servers
-------
.. autoclass:: ExtendedBarServer
  :members:
  :inherited-members:

.. autoclass:: ExtendedCaseServer
  :members:
  :exclude-members: label_prefix
  :inherited-members:

  .. autoattribute:: label_prefix
     :annotation:

.. autoclass:: ExtendedNodeServer
  :members:
  :inherited-members:


.. _attributes:

Selections
----------

.. autoclass:: ExtendedSelectionFactory
   :members:
