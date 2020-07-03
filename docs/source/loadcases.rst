Load cases
==========

**autoRobot** provides the following tools to interact with load cases in
the model.

.. _case_object:

Simple case object
------------------

.. autoclass:: autorobot.cases.ExtendedSimpleCase
  :members:
  :inherited-members:


.. _case_server:

Case server
-----------

.. autoclass:: autorobot.cases.ExtendedCaseServer
  :members:
  :exclude-members: label_prefix
  :inherited-members:

  .. autoattribute:: label_prefix
     :annotation:
