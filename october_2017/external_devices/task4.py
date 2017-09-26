from spynnaker.pyNN.external_devices_models \
    import AbstractEthernetTranslator
from spynnaker.pyNN.external_devices_models \
    import AbstractMulticastControllableDevice

import spynnaker8 as p


class MyEthernetDevice(AbstractMulticastControllableDevice):

    @property
    def device_control_key(self):
        return 1

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
        return "MyEthernetDevice"


class MyEthernetTranslator(AbstractEthernetTranslator):

    def translate_control_packet(self, multicast_packet):
        print "Received", multicast_packet.key, multicast_packet.payload


p.setup(1.0)

pop = p.Population(1, p.SpikeSourcePoisson(rate=100))
ethernet_device_control = p.external_devices.ExternalDeviceLifControl(
    devices=[MyEthernetDevice()], create_edges=False,
    translator=MyEthernetTranslator())
ethernet_device = p.external_devices.EthernetControlPopulation(
    1, ethernet_device_control)

ethernet_device.record("v")

p.Projection(
    pop, ethernet_device, p.OneToOneConnector(), p.StaticSynapse(weight=1.0))

p.run(1000)

print ethernet_device.get_data("v").segments[0].filter(name='v')

p.end()
