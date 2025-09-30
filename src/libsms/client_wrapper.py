import abc
import asyncio
import functools
import io
from pathlib import Path
from typing import Any, Callable, Coroutine, TypeVar, override

import httpx
import polars

from libsms._client.errors import UnexpectedStatus

from ._client import Client
from ._client.api.analyses.fetch_experiment_analysis import asyncio_detailed as fetch_experiment_analysis_async
from ._client.api.analyses.get_analysis_status import asyncio_detailed as get_analysis_status_async
from ._client.api.analyses.get_analysis_tsv import asyncio_detailed as get_analysis_tsv_async
from ._client.api.analyses.run_experiment_analysis import asyncio_detailed as run_analysis_async
from ._client.api.simulations.get_ecoli_simulation import asyncio_detailed as get_simulation_async
from ._client.api.simulations.get_ecoli_simulation_data import asyncio_detailed as get_simulation_data_async
from ._client.api.simulations.get_ecoli_simulation_status import asyncio_detailed as get_simulation_status_async
from ._client.api.simulations.run_ecoli_simulation import asyncio_detailed as run_simulation_async
from ._client.models import (
    BodyRunEcoliSimulation,
    EcoliSimulationDTO,
    ExperimentAnalysisDTO,
    ExperimentAnalysisRequest,
    ExperimentRequest,
    HTTPValidationError,
    OutputFile,
    SimulationRun,
)
from ._client.types import Response

T = TypeVar("T")


def retry(
    max_retries: int = 5,
    backoff: float = 1.0,
    exceptions: tuple[type[BaseException], ...] = (
        httpx.TimeoutException,
        httpx.ConnectError,
        asyncio.TimeoutError,
        httpx.HTTPStatusError,
        UnexpectedStatus,
    ),
) -> Callable[[Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]]:
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0
            delay = backoff
            while True:
                attempt += 1
                try:
                    result = await func(*args, **kwargs)
                    if hasattr(result, "status_code") and result.status_code >= 500:
                        raise httpx.HTTPStatusError(
                            f"Server error {result.status_code}",
                            request=httpx.Request("GET", "http://example.com"),
                            response=httpx.Response(
                                status_code=result.status_code,
                                request=httpx.Request("GET", "http://example.com"),
                                content=b"",
                            ),
                        )
                    return result
                except exceptions as e:
                    if attempt >= max_retries:
                        print(f"Giving up after {attempt} attempts")
                        raise
                    _arrow = ("=" * attempt) + ">"
                    print(f"{_arrow} ...Fetching data...")
                    # print(f"Caught {type(e).__name__}, retrying in {delay}s (attempt {attempt})...")
                    await asyncio.sleep(delay)
                    delay *= 2

        return wrapper

    return decorator


class ClientWrapper(abc.ABC):
    """
    A wrapper for the client that provides a consistent interface for making requests.
    """

    base_url: str
    api_client: Client | None = None
    httpx_client: httpx.Client | None = None

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or self._base_url()

    @abc.abstractmethod
    def _base_url(self) -> str:
        pass

    def _get_api_client(self) -> Client:
        if self.api_client is None:
            self.httpx_client = httpx.Client(base_url=self.base_url)
            self.api_client = Client(base_url=self.base_url, raise_on_unexpected_status=True)
            self.api_client.set_httpx_client(self.httpx_client)
        return self.api_client

    @retry(max_retries=10)
    async def run_simulation(self, request: ExperimentRequest) -> EcoliSimulationDTO:
        """Launch a vEcoli simulation."""
        api_client = self._get_api_client()
        response: Response[EcoliSimulationDTO | HTTPValidationError] = await run_simulation_async(
            client=api_client, body=BodyRunEcoliSimulation(request=request)
        )
        if response.status_code == 200 and isinstance(response.parsed, EcoliSimulationDTO):
            return response.parsed
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def get_simulation(self, database_id: int) -> EcoliSimulationDTO:
        """Get an uploaded simulation spec from the database."""
        api_client = self._get_api_client()
        response: Response[EcoliSimulationDTO | HTTPValidationError] = await get_simulation_async(
            client=api_client, id=database_id
        )
        if response.status_code == 200 and isinstance(response.parsed, EcoliSimulationDTO):
            return response.parsed
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def get_simulation_status(self, simulation: EcoliSimulationDTO) -> SimulationRun:
        """Get the status of a running simulation."""
        api_client = self._get_api_client()
        response: Response[SimulationRun | HTTPValidationError] = await get_simulation_status_async(
            client=api_client, id=simulation.database_id
        )
        if response.status_code == 200 and isinstance(response.parsed, SimulationRun):
            return response.parsed
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def run_analysis(self, request: ExperimentAnalysisRequest) -> ExperimentAnalysisDTO:
        """Run a simulation analysis on existing simulation results."""
        api_client = self._get_api_client()
        response: Response[ExperimentAnalysisDTO | HTTPValidationError] = await run_analysis_async(
            client=api_client, body=request
        )
        if response.status_code == 200 and isinstance(response.parsed, ExperimentAnalysisDTO):
            return response.parsed
        else:
            # raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")
            raise UnexpectedStatus(
                status_code=response.status_code,
                content=bytes(
                    f"Unexpected response status: {response.status_code}, detail: {response.content.decode()}".encode()
                ),
            )

    @retry(max_retries=10)
    async def get_analysis(self, database_id: int) -> ExperimentAnalysisDTO:
        """Get an uploaded analysis spec from the database."""
        api_client = self._get_api_client()
        response: Response[ExperimentAnalysisDTO | HTTPValidationError] = await fetch_experiment_analysis_async(
            client=api_client, id=database_id
        )
        if response.status_code == 200 and isinstance(response.parsed, ExperimentAnalysisDTO):
            return response.parsed
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def get_analysis_status(self, analysis: ExperimentAnalysisDTO) -> SimulationRun:
        """Get the status of a running analysis."""
        api_client = self._get_api_client()
        response: Response[SimulationRun | HTTPValidationError] = await get_analysis_status_async(
            client=api_client, id=analysis.database_id
        )
        if response.status_code == 200 and isinstance(response.parsed, SimulationRun):
            return response.parsed
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def get_tsv_outputs(self, analysis: ExperimentAnalysisDTO, outfile: Path | None = None) -> list[OutputFile]:
        """Get the tsv outputs of a given simulation analysis: (ptools)"""
        api_client = self._get_api_client()
        response: Response[list[OutputFile] | HTTPValidationError] = await get_analysis_tsv_async(
            client=api_client, id=analysis.database_id
        )
        if response.status_code == 200 and isinstance(response.parsed, list):
            outputs = response.parsed
            if outfile is not None:
                lines = ["".join(output.content).split("\n") for output in outputs]
                if outfile is not None:
                    with open(outfile, "w") as f:
                        for item in lines:
                            f.write(f"{item}\n")

            return outputs

        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")

    @retry(max_retries=10)
    async def get_simulation_data(
        self,
        experiment_id: str,
        lineage: int = 6,
        generation: int = 1,
        obs: list[str] | None = None,
        variant: int = 0,
        agent_id: int = 0,
    ) -> polars.DataFrame:
        """Get the requested simulation data results (parquet) as a polars dataframe.

        :param experiment_id: (str) Experiment ID of the given queried simulation. Note: this ID must refer to a simulation that has already been run.
        :param obs: (list[str]) List of observable names, in hive partition format, that you wish to retrieve from the output results. Note: this function
            aggregates and slices the vEcoli simulation parquet output. Refer to vEcoli documentation for more details on column labels.
        :param lineage: (int): Lineage seed ID from which results will be fetched.
        :param generation: (int) Generation ID from which results will be fetched. Defaults to `1`.
        :param variant: (int) Variant ID from which results will be fetched. Defaults to `0`.
        :param agent_id: (int): Agent ID from which results will be fetched. Defaults to `1`.
        :return: `polars.DataFrame` of requested simulation output data
        """
        api_client = self._get_api_client()
        response = await get_simulation_data_async(
            client=api_client,
            body=obs or ["bulk"],
            experiment_id=experiment_id,
            lineage_seed=lineage,
            generation=generation,
            variant=variant,
            agent_id=agent_id,
        )
        if response.status_code == 200:
            # return response.parsed
            return polars.from_dicts(response.parsed).sort("time")  # type: ignore[arg-type]
        else:
            raise TypeError(f"Unexpected response status: {response.status_code}, content: {type(response.content)}")


class ClientAcademic(ClientWrapper):
    @override
    def _base_url(self) -> str:
        return "https://sms.cam.uchc.edu"


class ClientLocal(ClientWrapper):
    def __init__(self, port: int = 8888, base_url: str | None = None):
        super().__init__(base_url)
        self.port = port

    @override
    def _base_url(self) -> str:
        return "http://localhost"


class SmsApi(ClientAcademic):
    pass


def format_tsv_string(output: OutputFile) -> str:
    """
    Convert a raw string containing escaped \\t and \\n into a proper TSV text.
    """
    raw_string = output.content
    return raw_string.encode("utf-8").decode("unicode_escape")


def tsv_string_to_polars_df(output: OutputFile) -> polars.DataFrame:
    """
    Parse a TSV-formatted string into a Polars DataFrame.
    """
    formatted = format_tsv_string(output)
    return polars.read_csv(io.StringIO(formatted), separator="\t")
