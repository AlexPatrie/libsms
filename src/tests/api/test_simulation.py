import pytest
from pathlib import Path
import asyncio

from libsms import api, utils, data_model as dm


@pytest.mark.asyncio
async def test_run_simulation(max_retries: int, delay: float) -> None:
    config_id = "sms"
    experiment = await api.run_simulation(config_id=config_id, max_retries=max_retries, delay_s=delay, verbose=True)
    assert experiment is not None
    utils.plog('test_run_simulation', experiment)


@pytest.mark.asyncio
async def test_get_status(example_experiment: dm.EcoliExperiment) -> None:
    experiment = example_experiment
    status = await api.check_simulation_status(experiment=experiment)
    assert status is not None
    assert "status" in status.model_dump().keys()
    utils.plog('test_get_status', status)


@pytest.mark.asyncio
async def test_get_analysis_manifest(example_experiment: dm.EcoliExperiment) -> None:
    experiment = example_experiment
    manifest = await api.get_analysis_manifest(experiment=experiment)
    # assert manifest is not None
    # assert isinstance(manifest.values()[0], list)
    utils.plog('test_get_analysis_manifest', manifest)
