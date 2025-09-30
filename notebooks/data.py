import marimo

__generated_with = "0.16.3"
app = marimo.App(width="full")


@app.cell
async def _():
    from libsms import sms_api

    base_url = "https://sms.cam.uchc.edu"
    expid = "sms_multigeneration"
    lineage_seed = 6
    generation = 1
    observables = ["bulk", "listeners__rnap_data__termination_loss"]

    # client = ClientAcademic(base_url=base_url)
    df = await sms_api.get_simulation_data(
        experiment_id=expid, lineage=lineage_seed, generation=generation, obs=observables
    )
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df.plot.line(x="time", y="listeners__rnap_data__termination_loss")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
