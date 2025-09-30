import asyncio

import pytest

from libsms._client.models import (
    ExperimentAnalysisRequest,
    OutputFile,
)
from libsms.client_wrapper import ClientAcademic, tsv_string_to_polars_df


@pytest.mark.asyncio
async def test_run_analysis(base_url: str, analysis_request: ExperimentAnalysisRequest) -> None:
    client = ClientAcademic(base_url=base_url)
    attempt = 0
    max_retries = 5
    backoff = 1.0
    while True:
        attempt += 1
        try:
            analysis = await client.run_analysis(request=analysis_request)
            print(analysis)
            break
        except:
            if attempt >= max_retries:
                raise
            print(f"Timeout, retrying in {backoff} seconds... (attempt {attempt})")
            await asyncio.sleep(backoff)
            backoff *= 2  # optional exponential backoff


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
    client = ClientAcademic(base_url=base_url)
    analysis = await client.get_analysis(database_id=dbid)
    outputs: list[OutputFile] = await client.get_tsv_outputs(analysis=analysis)
    output_i = outputs[0]
    df = tsv_string_to_polars_df(output_i)
    print(df)
