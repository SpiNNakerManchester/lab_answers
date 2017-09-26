import pyNN.spiNNaker as p
from spynnaker8.utilities.data_holder import DataHolder

from pacman.model.graphs.application.application_spinnaker_link_vertex \
    import ApplicationSpiNNakerLinkVertex


class MySpiNNakerLinkDevice(ApplicationSpiNNakerLinkVertex):

    def __init__(
            self, n_neurons, spinnaker_link_id, label=None):
        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_neurons, spinnaker_link_id, label=label)


class MySpiNNakerLinkDeviceDataHolder(DataHolder):

    def __init__(self, spinnaker_link_id, label=None):
        DataHolder.__init__(
            self, {"spinnaker_link_id": spinnaker_link_id, "label": label})

    @staticmethod
    def build_model():
        return MySpiNNakerLinkDevice


p.setup(1.0)

poisson = p.Population(1, p.SpikeSourcePoisson(rate=100))
device = p.Population(1, MySpiNNakerLinkDeviceDataHolder(spinnaker_link_id=1))

p.external_devices.activate_live_output_to(poisson, device)

p.run(100)

p.end()
