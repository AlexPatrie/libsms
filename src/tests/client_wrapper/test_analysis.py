import asyncio

import pytest

from libsms._client.errors import UnexpectedStatus
from libsms._client.models import OutputFile, ExperimentAnalysisRequest, ExperimentAnalysisRequestMultigeneration, ExperimentAnalysisRequestMultidaughter, ExperimentAnalysisRequestSingle
from libsms.client_wrapper import ClientWrapper, tsv_string_to_polars_df


async def test_run_analysis(base_url: str, analysis_request: ExperimentAnalysisRequest) -> None:
    client = ClientWrapper(base_url=base_url)
    analysis = await client.run_analysis(request=analysis_request)
    print(analysis)


async def run_analysis(base_url: str, analysis_request: ExperimentAnalysisRequest) -> None:
    client = ClientWrapper(base_url=base_url)
    analysis = await client.run_analysis(request=analysis_request)
    print(analysis)



@pytest.mark.asyncio
async def test_get_analysis() -> None:
    pass


@pytest.mark.asyncio
async def test_get_analysis_status() -> None:
    pass


@pytest.mark.asyncio
async def test_get_tsv_outputs() -> None:
    base_url = "https://sms.cam.uchc.edu"
    dbid = 1
    client = ClientWrapper(base_url=base_url)
    analysis = await client.get_analysis(database_id=dbid)
    outputs: list[OutputFile] = await client.get_tsv_outputs(analysis=analysis)
    output_i = outputs[0]
    df = tsv_string_to_polars_df(output_i)
    print(df)
