Extensions
==========

In order to focus on the model's data rather than the syntax, a layer of high-level methods is provided on top of the original functions.  Some .Net objects are encapsulated to provide new methods together with all the original methods and attributes.

.. automodule:: autorobot.extensions
   :members:
   :exclude-members: ExtendedNodeServer, ExtendedBarServer, ExtendedCaseServer, Capsule, ExtendedServer, app

   .. _servers: 
   
   Servers
   -------
   .. autoclass:: ExtendedBarServer
      :members:
      :inherited-members:
      :exclude-members: select
      
      

   .. autoclass:: ExtendedCaseServer
      :members:
      :inherited-members:

   .. autoclass:: ExtendedNodeServer
      :members:
      :inherited-members:
      

   .. _attributes:

   Attributes
   ----------
   .. autodata:: app
      :annotation: