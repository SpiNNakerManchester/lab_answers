from spynnaker.pyNN.external_devices_models import AbstractEthernetSensor
from spynnaker.pyNN.connections import SpynnakerLiveSpikesConnection
import time

import spynnaker8 as p


class MyEthernetSensor(AbstractEthernetSensor):

    def __init__(self):
        self._live_spikes_connection = SpynnakerLiveSpikesConnection(
            send_labels=["MyEthernetSensor"])
        self._live_spikes_connection.add_start_callback(
            "MyEthernetSensor", MyEthernetSensor._send_spike)

    @staticmethod
    def _send_spike(label, sender):
        time.sleep(0.01)
        print "Sending spike to 0"
        sender.send_spike(label, 0)

    def get_n_neurons(self):
        return 1

    def get_injector_label(self):
        return "MyEthernetSensor"

    def get_injector_parameters(self):
        return {}

    def get_translator(self):
        return None

    def get_database_connection(self):
        return self._live_spikes_connection


p.setup(1.0)

ethernet_sensor = p.external_devices.EthernetSensorPopulation(
    MyEthernetSensor())
ethernet_input_pop = p.Population(1, p.IF_curr_exp())

ethernet_input_pop.record("v")


p.Projection(
    ethernet_sensor, ethernet_input_pop, p.OneToOneConnector(),
    p.StaticSynapse(weight=1.0))

p.run(1000)

print ethernet_input_pop.get_data("v").segments[0].filter(name='v')

p.end()
