import marimo

__generated_with = "0.15.2"
app = marimo.App(width="full")


@app.cell
def _():
    import uuid
    from enum import StrEnum

    import marimo as mo

    from libsms._client.errors import UnexpectedStatus
    from libsms._client.models import (
        OutputFile, 
        ExperimentAnalysisRequest, 
        ExperimentAnalysisRequestSingle, 
        ExperimentAnalysisRequestMultidaughter,
        ExperimentAnalysisRequestMultigeneration,
        ExperimentAnalysisRequestMultiseed,
        ExperimentAnalysisRequestMultivariant,
        ExperimentAnalysisRequestMultiexperiment
    )

    from libsms.client_wrapper import AsyncClientWrapper, SyncClientWrapper, tsv_string_to_polars_df

    base_url = "https://sms.cam.uchc.edu"
    sync_client = SyncClientWrapper(base_url=base_url)
    async_client = AsyncClientWrapper(base_url=base_url)
    return ExperimentAnalysisRequest, StrEnum, mo, sync_client, uuid


@app.cell
def _(mo):
    getId, setId = mo.state(None)
    getAnalysis, setAnalysis = mo.state(None)
    getStatus, setStatus = mo.state(None)
    return getAnalysis, getId, getStatus, setAnalysis, setId, setStatus


@app.cell
def _(mo, setId, uuid):
    analysis_id_input = mo.ui.text(label="Enter Analysis ID", kind="text", value="sms_api", on_change=lambda val: setId(f"{val}-{uuid.uuid4()!s}"))
    analysis_id_input
    return


@app.cell
def _(getId):
    getId()
    return


@app.cell
def _(
    ExperimentAnalysisRequest,
    StrEnum,
    getId,
    setAnalysis,
    sync_client,
    uuid,
):
    class ApiScope(StrEnum):
        SIMULATION = "sim"
        ANALYSIS = "analysis"

    def unique_id(scope: ApiScope) -> str:
        return f"libsms-pytest-{scope}-{uuid.uuid4()!s}"


    def run_analysis():
        analysis_payload = {
            "experiment_id": "sms_multigeneration",
            "analysis_name": getId(),
            "single": {"ptools_rxns": {"n_tp": 8}, "ptools_rna": {"n_tp": 8}, "ptools_proteins": {"n_tp": 8}},
            "multidaughter": {},
            "multigeneration": {"ptools_rxns": {"n_tp": 8}, "ptools_rna": {"n_tp": 8}, "ptools_proteins": {"n_tp": 8}},
            "multiseed": {"ptools_rxns": {"n_tp": 8}, "ptools_rna": {"n_tp": 8}, "ptools_proteins": {"n_tp": 8}},
            "multivariant": {},
            "multiexperiment": {},
        }
        analysis_request = ExperimentAnalysisRequest.from_dict(analysis_payload)
        try:
            analysis = sync_client.run_analysis(request=analysis_request)
        except:
            analysis = sync_client.run_analysis(request=analysis_request)

        setAnalysis(analysis)
    return (run_analysis,)


@app.cell
def _(mo, run_analysis):
    runbtn = mo.ui.button(label="Run Analysis", on_click=lambda _: run_analysis())
    runbtn
    return


@app.cell
def _(getAnalysis):
    getAnalysis()
    return


@app.cell
def _(getAnalysis, setStatus, sync_client):
    def check_status():
        analysis = getAnalysis()
        if analysis is not None:
            status = sync_client.get_analysis_status(analysis=analysis)
            setStatus(status)
    return (check_status,)


@app.cell
def _(check_status, mo):
    statbtn = mo.ui.button(label="Check Status", on_click=lambda _: check_status())
    return (statbtn,)


@app.cell
def _(statbtn):
    statbtn
    return


@app.cell
def _(getStatus):
    getStatus()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
