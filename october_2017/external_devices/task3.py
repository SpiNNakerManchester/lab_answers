from spynnaker.pyNN.external_devices_models \
    import AbstractMulticastControllableDevice
from spinn_front_end_common.abstract_models import (
    ApplicationSpiNNakerLinkVertex)

import pyNN.spiNNaker as p


class MySpiNNakerLinkDevice(
        ApplicationSpiNNakerLinkVertex, AbstractMulticastControllableDevice):

    @property
    def device_control_key(self):
        return 0

    @property
    def device_control_max_value(self):
        return 100

    @property
    def device_control_min_value(self):
        return 0

    @property
    def device_control_uses_payload(self):
        return True

    @property
    def device_control_timesteps_between_sending(self):
        return 10

    @property
    def device_control_partition_id(self):
        return "MySpiNNakerLinkDevice"


p.setup(1.0)

pop = p.Population(1, p.SpikeSourcePoisson(rate=100))
spinnaker_link_device_control = p.external_devices.ExternalDeviceLifControl(
    devices=[MySpiNNakerLinkDevice(n_atoms=1, spinnaker_link_id=1)],
    create_edges=True)
spinnaker_link_device = p.Population(1, spinnaker_link_device_control)

spinnaker_link_device.record("v")

p.Projection(
    pop, spinnaker_link_device, p.OneToOneConnector(),
    p.StaticSynapse(weight=1.0))

p.run(1000)

print(spinnaker_link_device.get_data("v").segments[0].filter(name='v'))

p.end()
