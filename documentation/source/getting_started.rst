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

Quick Example
=============

Here’s the simplest way to run a full vEcoli workflow via the SMS REST API:

.. code-block:: python

    from libsms ecoli_experiment, simulation_status, analysis_manifest

    # 1.) Generate and run a simulation experiment
    # ========================================== #
    config_id = "sms"  # config id for the "core" single-cell simulation
    experiment = ecoli_experiment(config_id=config_id)

    # 2.) Check the simulation experiment status
    # ======================================== #
    status = simulation_status(experiment=experiment)

    # 3.) Get manifest of available analysis outputs
    # ============================================ #
    if status["status"].lower() == "completed":
        available_analysis_outputs = analysis_manifest(experiment=experiment)
        print(available_analysis_outputs)
