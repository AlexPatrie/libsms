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

    from libsms import sms_api, models

    # 1.) Generate and run a simulation experiment
    # ========================================== #
    experiment_id = "my_test_simulation"
    simulation = await sms_api.run_simulation(
        request=models.ExperimentRequest(experiment_id=experiment_id, simulation_name=experiment_id)
    )

    # 2.) Check the simulation experiment status
    # ======================================== #
    current_status = sms_api.get_simulation_status(simulation=simulation)

    # 3.) Get the simulation outputs, indexed by requested column(s)
    # ============================================================ #
    if current_status.status.lower() == "completed":
        observables = ["bulk", "listeners__rnap_data__termination_loss"]
        df: "polars.DataFrame" = await sms_api.get_simulation_data(experiment_id=simulation.experiment_id, obs=observables)
