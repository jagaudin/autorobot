Constants
=========

Some aliases for the Robot API enums. All the classes below are subclasses of
`IntEnum <https://docs.python.org/3/library/enum.html#intenum>`_ which means
they support iteration.

.. tip::

  The most-often used enums are imported at the top-level of the
  autorobot package for convenience, making them available as
  ``autorobot.RProjType`` for example. Of course, these enums are also available
  as attributes of the ``constants`` submodule. By contrast, the less
  commonly used enums do not have top-level shortcuts and need to be imported
  from the ``constants`` submodule.

.. automodule:: autorobot.constants

.. _const_types:

Types
-----

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

.. autoclass:: autorobot.RCaseNature
   :no-members:

   .. autoattribute:: PERM
      :annotation:  = IRobotCaseNature.I_CN_PERMANENT
   .. autoattribute:: IMPOSED
      :annotation:  = IRobotCaseNature.I_CN_EXPLOATATION
   .. caution:: The typo is **in Robot API**, not this document
   .. autoattribute:: WIND
      :annotation:  = IRobotCaseNature.I_CN_WIND
   .. autoattribute:: SNOW
      :annotation:  = IRobotCaseNature.I_CN_SNOW
   .. autoattribute:: ACC
      :annotation:  = IRobotCaseNature.I_CN_ACCIDENTAL

.. autoclass:: autorobot.RCaseType
   :no-members:

   .. autoattribute:: SIMPLE
      :annotation:  = IRobotCaseType.I_CT_SIMPLE
   .. autoattribute:: COMB
      :annotation:  = IRobotCaseType.I_CT_COMBINATION

.. autoclass:: autorobot.RCombType
   :no-members:

   .. autoattribute:: SLS
      :annotation:  = IRobotCombinationType.I_CBT_SLS
   .. autoattribute:: ULS
      :annotation:  = IRobotCombinationType.I_CBT_ULS

.. autoclass:: autorobot.RAnalysisType
   :no-members:

   .. autoattribute:: LINEAR
      :annotation:  = IRobotCaseAnalizeType.I_CAT_STATIC_LINEAR
   .. autoattribute:: NON_LIN
      :annotation:  = IRobotCaseAnalizeType.I_CAT_STATIC_NONLINEAR
   .. autoattribute:: COMB_LINEAR
      :annotation:  = IRobotCaseAnalizeType.I_CAT_COMB
   .. autoattribute:: COMB_NON_LIN
      :annotation:  = IRobotCaseAnalizeType.I_CAT_COMB_NONLINEAR

.. autoclass:: ROType
   :no-members:

   .. autoattribute:: BAR
      :annotation:  = IRobotObjectType.I_OT_BAR
   .. autoattribute:: CASE
      :annotation:  = IRobotObjectType.I_OT_CASE
   .. autoattribute:: NODE
      :annotation:  = IRobotObjectType.I_OT_NODE

.. autoclass:: RLabelType
   :no-members:

   .. autoattribute:: BAR_SECT
      :annotation:  = IRobotLabelType.I_LT_BAR_SECTION
   .. autoattribute:: MAT
      :annotation:  = IRobotLabelType.I_LT_MATERIAL
   .. autoattribute:: SUPPORT
      :annotation:  = IRobotLabelType.I_LT_SUPPORT
   .. autoattribute:: RELEASE
      :annotation:  = IRobotLabelType.I_LT_BAR_RELEASE

.. autoclass:: RMatType
   :no-members:

   .. autoattribute:: STEEL
      :annotation:  = IRobotMaterialType.I_MT_STEEL
   .. autoattribute:: ALUM
      :annotation:  = IRobotMaterialType.I_MT_ALUMINIUM
   .. autoattribute:: TIMBER
      :annotation:  = IRobotMaterialType.I_MT_TIMBER
   .. autoattribute:: CONCRETE
      :annotation:  = IRobotMaterialType.I_MT_CONCRETE
   .. autoattribute:: OTHER
      :annotation:  = IRobotMaterialType.I_MT_OTHER

.. autoclass:: RReleaseValues
   :no-members:

   .. autoattribute:: NONE
      :annotation:  = IRobotBarEndReleaseValue.I_BERV_NONE
   .. autoattribute:: STD
      :annotation:  = IRobotBarEndReleaseValue.I_BERV_STD
   .. autoattribute:: FIXED
      :annotation:  = IRobotBarEndReleaseValue.I_BERV_FIXED

.. autoclass:: RLoadType
   :no-members:

   .. autoattribute:: DEAD
      :annotation:  = IRobotLoadRecordType.I_LRT_DEAD
   .. autoattribute:: NODAL
      :annotation:  = IRobotLoadRecordType.I_LRT_NODE_FORCE
   .. autoattribute:: BAR_UDL
      :annotation:  = IRobotLoadRecordType.I_LRT_BAR_UNIFORM
   .. autoattribute:: BAR_PL
      :annotation:  = IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED


.. _const_bar_loads:

Bar loads
---------

.. autoclass:: RBarPLValues
.. autoclass:: RBarUDLValues


.. _const_license:

License
-------

.. autoclass:: RLicense
.. autoclass:: RLicenseStatus
