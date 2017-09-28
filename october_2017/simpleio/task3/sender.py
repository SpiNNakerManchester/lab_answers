import pyNN.spiNNaker as p
import time
import sys
import logging

logging.basicConfig()


def send_spike(label, sender):
    time.sleep(0.01)
    print "Sending spike to neuron 0"
    sender.send_spike(label, 0)


live_connection = p.external_devices.SpynnakerLiveSpikesConnection(
    send_labels=[sys.argv[1]], local_port=int(sys.argv[2]))
live_connection.add_start_callback(sys.argv[1], send_spike)
live_connection.join()
