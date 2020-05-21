Constants
=========

Some aliases for the Robot API enums.

.. tip:: The most-often used enums are imported at the top-level of the autorobot package for convenience, making them available as ``autorobot.ROType`` for example. Of course, these enums are also available as attributes of the ``constants`` submodule. By contrast, the less commonly used enums do not have top-level shortcuts and need to be imported from the ``constants`` submodule.

.. automodule:: autorobot.constants

.. _const_types:

Types
-----

.. autoclass:: autorobot.ROType
   :no-members:
   
   .. autoattribute:: BAR 
      :annotation:  = IRobotObjectType.I_OT_BAR
   .. autoattribute:: CASE
      :annotation:  = IRobotObjectType.I_OT_CASE
   .. autoattribute:: NODE
      :annotation:  = IRobotObjectType.I_OT_NODE
      
.. autoclass:: autorobot.RProjType
   :no-members:

   .. autoattribute:: BUILDING
      :annotation:  = IRobotProjectType.I_PT_BUILDING
   .. autoattribute:: FRAME_2D
      :annotation:  = IRobotProjectType.I_PT_FRAME_2D
   .. autoattribute:: FRAME_3D
      :annotation:  = IRobotProjectType.I_PT_FRAME_3D
   .. autoattribute:: SHELL
      :annotation:  = IRobotProjectType.I_PT_SHELL
   .. autoattribute:: TRUSS_2D
      :annotation:  = IRobotProjectType.I_PT_TRUSS_2D
   .. autoattribute:: TRUSS_3D
      :annotation:  = IRobotProjectType.I_PT_TRUSS_3D
   
.. autoclass:: RCaseType
   :no-members:
   
   .. autoattribute:: SIMPLE
      :annotation:  = IRobotCaseType.I_CT_SIMPLE
   .. autoattribute:: COMB
      :annotation:  = IRobotCaseType.I_CT_COMBINATION


.. autoclass:: RLoadType


.. _const_bar_loads:

Bar loads
---------

.. autoclass:: RBarPLValues
.. autoclass:: RBarUDLValues

