import logging
import sys
import datetime

import pytest

from libsms import data_model as dm


DEFAULT_MAX_RETRIES = 20
DEFAULT_DELAY = 1.0


@pytest.fixture(scope="function")
def max_retries() -> int:
    return DEFAULT_MAX_RETRIES


@pytest.fixture(scope="function")
def delay() -> float:
    return DEFAULT_DELAY


@pytest.fixture(scope="function")
def example_experiment() -> dm.EcoliExperiment:
    return dm.EcoliExperiment(
        experiment_id='sms-079c43c-1896956c5366',
        simulation=dm.EcoliWorkflowSimulation(
            sim_request=dm.EcoliWorkflowRequest(
                config_id='sms',
                simulator=dm.SimulatorVersion(
                    git_commit_hash='079c43c',
                    git_repo_url='https://github.com/CovertLab/vEcoli',
                    git_branch='master',
                    database_id=2,
                    created_at=datetime.datetime(2025, 8, 26, 0, 49, 30)
                ),
                overrides=dm.Overrides(config={}),
                variants=dm.Variants(config={}),
                parca_dataset_id=None
            ),
            database_id=None,
            slurmjob_id=760521
        ),
        last_updated='2025-09-10 21:42:44.133647',
        metadata={},
        experiment_tag='sms-079c43c-1896956c5366-760521'
    )




