import pytest

from libsms.client_wrapper import ClientWrapper


@pytest.mark.asyncio
async def test_get_simulation_data() -> None:
    base_url = "https://sms.cam.uchc.edu"
    expid = "sms_multigeneration"
    lineage_seed = 6
    generation = 1
    observables = ["bulk", "listeners__rnap_data__termination_loss"]

    client = ClientWrapper(base_url=base_url)
    data_response = await client.get_simulation_data(
        experiment_id=expid,
        lineage=lineage_seed,
        generation=generation,
        obs=observables
    )
    assert sorted(data_response.columns) == sorted(["bulk", "time", "listeners__rnap_data__termination_loss"])
    print(data_response)

