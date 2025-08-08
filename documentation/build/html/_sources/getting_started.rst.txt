================
Getting Started
================

Welcome to the libsms!

Installation
============

To install with PIP:

.. code-block:: bash

   pip install libsms

To install with an environment manager:
We hightly recommend using an environment manager like UV. Check out the documentation
for UV here: https://docs.astral.sh/uv/

.. code-block:: bash

    uv add libsms

Quick Example (getting observables data)
========================================

Here’s the simplest way to run it:

.. code-block:: python

   from libsms import get_observables_data

   obs = ["bulk", "time"]
   df = get_observables_data(observables=obs)
