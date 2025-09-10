import pytest

from libsms import api, utils
from libsms import data_model as dm


@pytest.mark.asyncio
async def test_run_simulation(max_retries: int, delay: float) -> None:
    config_id = "sms"
    experiment = api.ecoli_experiment(config_id=config_id, max_retries=max_retries, delay_s=delay, verbose=True)
    assert experiment is not None
    utils.plog("test_run_simulation", experiment)


@pytest.mark.asyncio
async def test_get_status(example_experiment: dm.EcoliExperiment) -> None:
    experiment = example_experiment
    status = api.simulation_status(experiment=experiment)
    assert status is not None
    assert "status" in status.model_dump().keys()
    utils.plog("test_get_status", status)


@pytest.mark.asyncio
async def test_get_analysis_manifest(example_experiment: dm.EcoliExperiment) -> None:
    experiment = example_experiment
    manifest = api.analysis_manifest(experiment=experiment)
    assert manifest is not None
    # assert isinstance(list(manifest.values)[0], list)
    utils.plog("test_get_analysis_manifest", manifest)
