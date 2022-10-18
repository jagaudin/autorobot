.. _about_synonyms:

Synonyms
========

In order to access some widely used constants without having to import
and refer to the ``IntEnum`` objects defined in the ``autorobot.constants``
submodule, the ``synonyms`` dictionary can be used to pass keyword strings
to functions that support it.

This means for example that a building project can be created
with: ::

    import autorobot as ar

    rb = ar.initialize()
    rb.new('BUILDING')  # Without synonyms: rb.new(ar.RProjType.BUILDING)

thereby avoiding to import and refer to ``autorobot.RProjType.BUILDING``.

This comes handy when creating load cases' combinations in particular.

.. tip:: The synonyms dictionary can be customized to suit preferences
  and accommodate specific needs in a script. ::

       import autorobot as ar
       from autorobot.synonyms import synonyms

       synonyms.update({
           'shell': ar.RProjType.SHELL  # Don't like all-capital words
           'RDA_ExcitDir': ar.RobotOM.IRobotDynamicAnalysisExcitationDirection  # Too long
       })
       ...
       # Casting to IRobotDynamicAnalysisExcitationDirection
       exc_dir = synonyms['RDA_ExcitDir'](seismic_params.ExcitationDir)

  When frequently used, a bespoke synonym dictionary can be saved and loaded
  with the `json <https://docs.python.org/3/library/json.html>`_ module. ::

       import json
       import autorobot as ar
       from autorobot.synonyms import synonyms

       with open('.\my_synonyms.json', 'r') as f:
           my_syn = json.load(f)
       synonyms.update(my_syn)
       ...
       with open('.\my_synonyms.json', 'w') as f:
           json.dump(my_syn, f, indent=2)

  This is limited to the capacity of the json serializer. To store e.g.
  .Net interface objects, subclasses of
  `JSONEncoder <https://docs.python.org/3/library/json.html#json.JSONEncoder>`_
  and
  `JSONDecoder <https://docs.python.org/3/library/json.html#json.JSONEncoder>`_
  could be used.

.. autodata:: autorobot.synonyms.synonyms
   :annotation:

   The predefined synonyms are:

    * ``'BUILDING'``: :py:data:`autorobot.RProjType` ``.BUILDING``
    * ``'FRAME_2D'``: :py:data:`autorobot.RProjType` ``.FRAME_2D``
    * ``'FRAME_3D'``: :py:data:`autorobot.RProjType` ``.FRAME_3D``
    * ``'SHELL'``: :py:data:`autorobot.RProjType` ``.SHELL``
    * ``'TRUSS_2D'``: :py:data:`autorobot.RProjType` ``.TRUSS_2D``
    * ``'TRUSS_3D'``: :py:data:`autorobot.RProjType` ``.TRUSS_3D``

    * ``'PERM'``: :py:data:`autorobot.RCaseNature` ``.PERM``
    * ``'IMPOSED'``: :py:data:`autorobot.RCaseNature` ``.IMPOSED``
    * ``'WIND'``: :py:data:`autorobot.RCaseNature` ``.WIND``
    * ``'SNOW'``: :py:data:`autorobot.RCaseNature` ``.SNOW``
    * ``'ACC'``: :py:data:`autorobot.RCaseNature` ``.ACC``

    * ``'SLS'``: :py:data:`autorobot.RCombType` ``.SLS``
    * ``'ULS'``: :py:data:`autorobot.RCombType` ``.ULS``

    * ``'LINEAR'``: :py:data:`autorobot.RAnalysisType` ``.LINEAR``
    * ``'NON_LIN'``: :py:data:`autorobot.RAnalysisType` ``.NON_LIN``
    * ``'COMB_LINEAR'``: :py:data:`autorobot.RAnalysisType` ``.COMB_LINEAR``
    * ``'COMB_NON_LIN'``: :py:data:`autorobot.RAnalysisType` ``.COMB_NON_LIN``
