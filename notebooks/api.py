import marimo

__generated_with = "0.15.2"
app = marimo.App(width="full")


@app.cell
def _():
    import asyncio
    from asyncio import sleep

    import httpx

    from libsms.data_model import EcoliExperiment

    return EcoliExperiment, asyncio, httpx, sleep


@app.cell
def _(EcoliExperiment, asyncio, client, httpx):
    from abc import abstractmethod

    class iclient:
        def __init__(
            self,
            max_retries: int | None = None,
            delay: float | None = None,
            verbose: bool | None = None,
            timeout: float | None = None,
        ):
            self.max_retries = max_retries or 20
            self.delay_s = delay or 1.0
            self.verbose = verbose or False
            self.timeout = timeout or 30.0

        @property
        async def value(self):
            return await self._execute(**self.params())

        @abstractmethod
        def params(self):
            pass

        @abstractmethod
        def method_type(self):
            pass

        @abstractmethod
        def url(self) -> str:
            pass

        @abstractmethod
        def body(self) -> dict | None:
            pass

        def get_url(self, **params):
            url = self.url()
            if params:
                url += "?"
                for pname, pval in params.items():
                    url += f"{pname}={pval}"
            return url

        async def _execute(
            self,
            **params,
        ) -> EcoliExperiment:
            method_type = self.method_type()
            max_retries = self.max_retries
            delay_s = self.delay_s
            verbose = self.verbose

            url = self.get_url(**params)
            method = client.post if method_type.lower() == "post" else client.get
            kwargs = {"url": url, "headers": {"Accept": "application/json"}, "timeout": self.timeout}
            if method_type.lower() == "post":
                kwargs["json"] = self.body()

            attempt = 0
            async with httpx.AsyncClient() as client:
                while attempt < max_retries:
                    attempt += 1
                    try:
                        if verbose:
                            print(f"Attempt {attempt}...")
                        response = await method(**kwargs)

                        response.raise_for_status()  # raises for 4xx/5xx

                        data = response.json()
                        if verbose:
                            print("Success on attempt", attempt)
                        return EcoliExperiment(**data)

                    except (httpx.RequestError, httpx.HTTPStatusError) as err:
                        if attempt == max_retries:
                            print(f"Attempt {attempt} failed:", err)
                            raise
                        await asyncio.sleep(delay_s)

    return


@app.cell
def _(EcoliExperiment, asyncio, httpx, sleep):
    async def run_simulation(
        config_id: str, max_retries: int = 20, delay_s: float = 1.0, verbose: bool = False
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
                    if verbose:
                        print(f"Attempt {attempt}...")
                    response = await client.post(
                        url,
                        json=body,
                        headers={"Accept": "application/json"},
                        timeout=30.0,  # optional, adjust as needed
                    )

                    response.raise_for_status()  # raises for 4xx/5xx

                    data = response.json()
                    if verbose:
                        print("Success on attempt", attempt)
                    return EcoliExperiment(**data)

                except (httpx.RequestError, httpx.HTTPStatusError) as err:
                    if attempt == max_retries:
                        print(f"Attempt {attempt} failed:", err)
                        raise
                    await asyncio.sleep(delay_s)

    async def check_simulation_status(
        experiment: EcoliExperiment | None, max_retries: int = 20, delay_s: float = 1.0, verbose: bool = False
    ) -> EcoliExperiment:
        if experiment is None:
            raise ValueError("Wait till the experiment is generated...")

        url = f"https://sms.cam.uchc.edu/wcm/simulation/run/status?experiment_tag={experiment.experiment_tag}"

        attempt = 0
        async with httpx.AsyncClient() as client:
            while attempt < max_retries:
                attempt += 1
                try:
                    if verbose:
                        print(f"Attempt {attempt}...")
                    response = await client.get(
                        url,
                        headers={"Accept": "application/json"},
                        timeout=30.0,  # optional, adjust as needed
                    )

                    response.raise_for_status()  # raises for 4xx/5xx

                    data = response.json()
                    if verbose:
                        print("Success on attempt", attempt)
                    return data

                except (httpx.RequestError, httpx.HTTPStatusError) as err:
                    if attempt == max_retries:
                        print(f"Attempt {attempt} failed:", err)
                        raise
                    await asyncio.sleep(delay_s)

    async def get_analysis_manifest(
        experiment: EcoliExperiment | None, max_retries: int = 20, delay_s: float = 1.0, verbose: bool = False
    ) -> EcoliExperiment:
        if experiment is None:
            raise ValueError("Wait till the experiment is generated...")

        url = f"https://sms.cam.uchc.edu/wcm/analysis/outputs?experiment_id={experiment.experiment_id}"

        attempt = 0
        async with httpx.AsyncClient() as client:
            while attempt < max_retries:
                attempt += 1
                try:
                    if verbose:
                        print(f"Attempt {attempt}...")
                    response = await client.get(
                        url,
                        headers={"Accept": "application/json"},
                        timeout=30.0,  # optional, adjust as needed
                    )

                    response.raise_for_status()  # raises for 4xx/5xx

                    data = response.json()
                    if verbose:
                        print("Success on attempt", attempt)
                    return data

                except (httpx.RequestError, httpx.HTTPStatusError) as err:
                    if attempt == max_retries:
                        print(f"Attempt {attempt} failed:", err)
                        raise
                    await asyncio.sleep(delay_s)

    async def onrun(config_id: str):
        # config_id = input("Enter the config ID (press enter to use default of sms_single): ") or "sms_single"
        print(f"Using config id: {config_id}")
        return await run_simulation(config_id=config_id)

    async def onstatus(experiment):
        stat = None
        if experiment is not None:
            await sleep(3.0)
            stat = await check_simulation_status(experiment=experiment)
            print(stat)
        return stat

    async def onmanifest(experiment):
        return await get_analysis_manifest(experiment=experiment)

    return onmanifest, onrun, onstatus


@app.cell
async def _(onrun):
    MAX_RETRIES = 20
    DELAY = 1.0

    config_id = input("Enter the config ID (press enter to use default of sms): ") or "sms"
    experiment = await onrun(config_id)
    experiment
    return (experiment,)


@app.cell
async def _(experiment, onmanifest, onstatus):
    status = await onstatus(experiment)
    if status["status"] == "completed":
        print(await onmanifest(experiment))
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
