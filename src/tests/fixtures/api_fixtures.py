import uuid
from enum import StrEnum

import pytest

from libsms._client.models import ExperimentAnalysisRequest, ExperimentRequest

DEFAULT_MAX_RETRIES = 20
DEFAULT_DELAY = 1.0


class ApiScope(StrEnum):
    SIMULATION = "sim"
    ANALYSIS = "analysis"


def unique_id(scope: ApiScope) -> str:
    return f"libsms-pytest-{scope}-{uuid.uuid4()!s}"


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://sms.cam.uchc.edu"


@pytest.fixture(scope="session")
def simulation_request() -> ExperimentRequest:
    sim_id = unique_id(scope=ApiScope.SIMULATION)
    payload = {
        "experiment_id": sim_id,
        "simulation_name": sim_id,
        "metadata": {},
        "run_parca": True,
        "generations": 1,
        "max_duration": 10800,
        "initial_global_time": 0,
        "time_step": 1,
        "single_daughters": True,
        "variants": {},
        "analysis_options": {},
        "division_variable": [],
        "add_processes": [],
        "exclude_processes": [],
        "processes": [],
        "process_configs": {},
        "topology": {},
        "engine_process_reports": [],
        "emit_paths": [],
        "inherit_from": [],
        "spatial_environment_config": {},
        "swap_processes": {},
        "flow": {},
        "initial_state_overrides": [],
        "initial_state": {},
    }
    return ExperimentRequest.from_dict(payload)


@pytest.fixture(scope="session")
def analysis_request() -> ExperimentAnalysisRequest:
    analysis_id = unique_id(scope=ApiScope.ANALYSIS)
    payload = {
        "experiment_id": "sms_multigeneration",
        "analysis_name": analysis_id,
        "single": {},
        "multidaughter": {},
        "multigeneration": {"ptools_rxns": {"n_tp": 8}, "ptools_rna": {"n_tp": 8}, "ptools_proteins": {"n_tp": 8}},
        "multiseed": {},
        "multivariant": {},
        "multiexperiment": {},
    }
    return ExperimentAnalysisRequest.from_dict(payload)
