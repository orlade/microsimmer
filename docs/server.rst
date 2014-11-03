========
 Server
========

The server layer listens for incoming requests from the Web, and parses them
into native objects. These requests are delegated to the middleware layer to get
results, which are in turn serialised back to whatever format the client wants.

.. automodule:: host.server.Server
   :members:


Methods
=======

.. autoclass:: host.server.Server.Server
   :members:

