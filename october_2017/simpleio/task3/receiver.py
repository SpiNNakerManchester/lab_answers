import pyNN.spiNNaker as p
import sys
import logging

logging.basicConfig()


def receive_spikes(label, time, neuron_ids):
    print "Received spikes from population {}, neurons {} at time {}".format(
        label, neuron_ids, time)


live_connection = p.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=[sys.argv[1]], local_port=int(sys.argv[2]))
live_connection.add_receive_callback(sys.argv[1], receive_spikes)
live_connection.join()
