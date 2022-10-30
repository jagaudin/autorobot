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

.. _const_types:

Types
-----

.. autodata:: autorobot.RProjType
   :annotation:

   * ``BUILDING``: ``IRobotProjectType.I_PT_BUILDING``
   * ``FRAME_2D``: ``IRobotProjectType.I_PT_FRAME_2D``
   * ``FRAME_3D``: ``IRobotProjectType.I_PT_FRAME_3D``
   * ``SHELL``: ``IRobotProjectType.I_PT_SHELL``
   * ``TRUSS_2D``: ``IRobotProjectType.I_PT_TRUSS_2D``
   * ``TRUSS_3D``: ``IRobotProjectType.I_PT_TRUSS_3D``

.. autodata:: autorobot.RCaseNature
   :annotation:

   * ``PERM``: ``IRobotCaseNature.I_CN_PERMANENT``
   * ``IMPOSED``: ``IRobotCaseNature.I_CN_EXPLOATATION``
   * ``WIND``: ``IRobotCaseNature.I_CN_WIND``
   * ``SNOW``: ``IRobotCaseNature.I_CN_SNOW``
   * ``ACC``: ``IRobotCaseNature.I_CN_ACCIDENTAL``

   .. caution:: The typo in ``I_CN_EXPLOATATION`` is **in Robot API**, not this document

.. autodata:: autorobot.RCaseType
   :annotation:

   * ``SIMPLE``: ``IRobotCaseType.I_CT_SIMPLE``
   * ``COMB``: ``IRobotCaseType.I_CT_COMBINATION``

.. autodata:: autorobot.RCombType
   :annotation:

   * ``SLS``: ``IRobotCombinationType.I_CBT_SLS``
   * ``ULS``: ``IRobotCombinationType.I_CBT_ULS``

.. autodata:: autorobot.RAnalysisType
   :annotation:

   * ``LINEAR``: ``IRobotCaseAnalizeType.I_CAT_STATIC_LINEAR``
   * ``NON_LIN``: ``IRobotCaseAnalizeType.I_CAT_STATIC_NONLINEAR``
   * ``COMB_LINEAR``: ``IRobotCaseAnalizeType.I_CAT_COMB``
   * ``COMB_NON_LIN``: ``IRobotCaseAnalizeType.I_CAT_COMB_NONLINEAR``

.. autodata:: autorobot.constants.ROType
   :annotation:

   * ``BAR``: ``IRobotObjectType.I_OT_BAR``
   * ``CASE``: ``IRobotObjectType.I_OT_CASE``
   * ``FE``: ``IRobotObjectType.I_OT_FINITE_ELEMENT``
   * ``GEOMETRY``: ``IRobotObjectType.I_OT_GEOMETRY``
   * ``GROUP``: ``IRobotObjectType.I_OT_FAMILY``
   * ``NODE``: ``IRobotObjectType.I_OT_NODE``
   * ``OBJECT``: ``IRobotObjectType.I_OT_OBJECT``
   * ``PANEL``: ``IRobotObjectType.I_OT_PANEL``
   * ``UNDEFINED``: ``IRobotObjectType.I_OT_UNDEFINED``
   * ``VOLUME``: ``IRobotObjectType.I_OT_VOLUME``

.. autodata:: autorobot.RLabelType
   :annotation:

   * ``BAR_SECT``: ``IRobotLabelType.I_LT_BAR_SECTION``
   * ``MAT``: ``IRobotLabelType.I_LT_MATERIAL``
   * ``SUPPORT``: ``IRobotLabelType.I_LT_SUPPORT``
   * ``RELEASE``: ``IRobotLabelType.I_LT_BAR_RELEASE``

.. autodata:: autorobot.constants.RMatType
   :annotation:

   * ``STEEL``: ``IRobotMaterialType.I_MT_STEEL``
   * ``ALUM``: ``IRobotMaterialType.I_MT_ALUMINIUM``
   * ``TIMBER``: ``IRobotMaterialType.I_MT_TIMBER``
   * ``CONCRETE``: ``IRobotMaterialType.I_MT_CONCRETE``
   * ``OTHER``: ``IRobotMaterialType.I_MT_OTHER``

.. autodata:: autorobot.constants.RReleaseValues
   :annotation:

   * ``NONE``: ``IRobotBarEndReleaseValue.I_BERV_NONE``
   * ``STD``: ``IRobotBarEndReleaseValue.I_BERV_STD``
   * ``FIXED``: ``IRobotBarEndReleaseValue.I_BERV_FIXED``

.. autodata:: autorobot.constants.RLoadType
   :annotation:

   * ``DEAD``: ``IRobotLoadRecordType.I_LRT_DEAD``
   * ``NODAL``: ``IRobotLoadRecordType.I_LRT_NODE_FORCE``
   * ``BAR_UDL``: ``IRobotLoadRecordType.I_LRT_BAR_UNIFORM``
   * ``BAR_PL``: ``IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED``


.. _const_bar_loads:

Bar loads
---------

.. autodata:: autorobot.constants.RDeadValues
   :annotation:

   * ``X``: ``IRobotDeadRecordValues.I_DRV_X``
   * ``Y``: ``IRobotDeadRecordValues.I_DRV_Y``
   * ``Z``: ``IRobotDeadRecordValues.I_DRV_Z``
   * ``COEFF``: ``IRobotDeadRecordValues.I_DRV_COEFF``
   * ``ENTIRE_STRUCT``: ``IRobotDeadRecordValues.I_DRV_ENTIRE_STRUCTURE``

.. autodata:: autorobot.constants.RBarPLValues
   :annotation:

   * ``X``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_X``
   * ``FX``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FX``
   * ``FY``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FY``
   * ``FZ``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FZ``
   * ``CX``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CX``
   * ``CY``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CY``
   * ``CZ``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CZ``
   * ``ALPHA``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_ALPHA``
   * ``BETA``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_BETA``
   * ``GAMMA``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_GAMMA``
   * ``GEN_NODE``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_GENERATE_CALC_NODE``
   * ``IS_LOC``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_LOC``
   * ``IS_REL``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_REL``
   * ``OFFSET_Y``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Y``
   * ``OFFSET_Z``: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Z``

.. autodata:: autorobot.constants.RBarUDLValues
   :annotation:

   * ``FX``: ``IRobotBarUniformRecordValues.I_BURV_PX``
   * ``FY``: ``IRobotBarUniformRecordValues.I_BURV_PY``
   * ``FZ``: ``IRobotBarUniformRecordValues.I_BURV_PZ``
   * ``ALPHA``: ``IRobotBarUniformRecordValues.I_BURV_ALPHA``
   * ``BETA``: ``IRobotBarUniformRecordValues.I_BURV_BETA``
   * ``GAMMA``: ``IRobotBarUniformRecordValues.I_BURV_GAMMA``
   * ``IS_LOC``: ``IRobotBarUniformRecordValues.I_BURV_LOCAL``
   * ``IS_PROJ``: ``IRobotBarUniformRecordValues.I_BURV_PROJECTION``
   * ``IS_REL``: ``IRobotBarUniformRecordValues.I_BURV_RELATIVE``
   * ``OFFSET_Y``: ``IRobotBarUniformRecordValues.I_BURV_OFFSET_Y``
   * ``OFFSET_Z``: ``IRobotBarUniformRecordValues.I_BURV_OFFSET_Z``

.. _const_editing:

Editing
-------

.. autodata:: autorobot.constants.REditOpt
   :annotation:

   * ``COPY``: ``IRobotTranslateOptions.COPY``
   * ``MOVE``: ``IRobotTranslateOptions.MOVE``


.. _const_license:

License
-------

.. autodata:: autorobot.constants.RLicense
   :annotation:

   * ``LOCAL``: ``IRobotLicenseEntitlement.I_LE_LOCAL_SOLVE``
   * ``CLOUD``: ``IRobotLicenseEntitlement.I_LE_CLOUD_SOLVE``

.. autodata:: autorobot.constants.RLicenseStatus
   :annotation:

   * ``OK``: ``IRobotLicenseEntitlementStatus.I_LES_ENTITLED``
