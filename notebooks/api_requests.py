import marimo

__generated_with = "0.15.2"
app = marimo.App(width="full")


@app.cell
def _():
    import requests
    from httpx import Client, QueryParams, HTTPStatusError

    def run_simulation(config_id: str):
        url = f"https://sms.cam.uchc.edu/wcm/simulation/run?config_id={config_id}"
        response = requests.post(url, headers={"Accept": "*/*"})
        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}")
        return response.json()


    def get_status(experiment: dict):
        tag = experiment['experiment_tag']
        url = f"https://sms.cam.uchc.edu/wcm/simulation/run/status?experiment_tag={tag}"
        response = requests.get(url, headers={"Accept": "*/*"})
        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}")
        return response.json()
    return get_status, run_simulation


@app.cell
def _(run_simulation):
    experiment = run_simulation(config_id="sms_single")
    experiment
    return (experiment,)


@app.cell
def _(experiment, get_status):
    status = get_status(experiment)
    status
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
