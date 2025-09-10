import marimo

__generated_with = "0.15.2"
app = marimo.App(width="full")


@app.cell
def _():
    import asyncio
    from textwrap import dedent
    from pprint import pp

    import httpx
    import marimo as mo

    from libsms.data_model import Overrides, Variants, EcoliExperiment
    return EcoliExperiment, asyncio, httpx, mo


@app.cell
def _(mo):
    get_experiment, set_experiment = mo.state(None)
    get_status, set_status = mo.state(None)
    return


@app.cell
def _(EcoliExperiment, asyncio, httpx):
    async def run_simulation(
        config_id: str,
        max_retries: int = 20,
        delay_s: float = 1.0 
    ) -> EcoliExperiment:
        url = f"https://sms.cam.uchc.edu/wcm/simulation/run?config_id={config_id}"
        body = {
            "overrides": {"config": {}},
            "variants": {"config": {}},
        }

        attempt = 0
        async with httpx.AsyncClient() as client:
            while attempt < max_retries:
                attempt += 1
                try:
                    print(f"Attempt {attempt}...")
                    response = await client.post(
                        url,
                        json=body,
                        headers={"Accept": "application/json"},
                        timeout=30.0,  # optional, adjust as needed
                    )

                    response.raise_for_status()  # raises for 4xx/5xx

                    data = response.json()
                    print("Success on attempt", attempt)
                    return EcoliExperiment(**data)

                except (httpx.RequestError, httpx.HTTPStatusError) as err:
                    if attempt == max_retries:
                        print(f"Attempt {attempt} failed:", err)
                        raise
                    await asyncio.sleep(delay_s)

    async def check_simulation_status(
        experiment: EcoliExperiment | None,
        max_retries: int = 20,
        delay_s: float = 1.0 
    ) -> EcoliExperiment:
        if experiment is None:
            raise ValueError("Wait till the experiment is generated...")

        url = f"https://sms.cam.uchc.edu/wcm/simulation/run/status?experiment_tag={experiment.experiment_tag}"

        attempt = 0
        async with httpx.AsyncClient() as client:
            while attempt < max_retries:
                attempt += 1
                try:
                    print(f"Attempt {attempt}...")
                    response = await client.get(
                        url,
                        headers={"Accept": "application/json"},
                        timeout=30.0,  # optional, adjust as needed
                    )

                    response.raise_for_status()  # raises for 4xx/5xx

                    data = response.json()
                    print("Success on attempt", attempt)
                    return data

                except (httpx.RequestError, httpx.HTTPStatusError) as err:
                    if attempt == max_retries:
                        print(f"Attempt {attempt} failed:", err)
                        raise
                    await asyncio.sleep(delay_s)

    async def onrun(*args):
        config_id = input("Enter the config ID (press enter to use default of sms_single): ") or "sms_single"
        print(f'Using config id: {config_id}')
        return await run_simulation(config_id=config_id, *args)
    return check_simulation_status, onrun


@app.cell
async def _(onrun):
    from asyncio import sleep

    MAX_RETRIES = 20
    DELAY = 1.0
    experiment = await onrun()
    experiment
    return experiment, sleep


@app.cell
def _(check_simulation_status, sleep):
    async def status(experiment):
        stat = None
        if experiment is not None:
            sleep(3.0)
            stat = await check_simulation_status(experiment=experiment)
            print(status)
        return stat
        
    return (status,)


@app.cell
async def _(experiment, status):
    await status(experiment)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
