"""
Synfirechain-like example
"""
import spynnaker8 as p
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt
import time

runtime = 10000
p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
nNeurons = 100  # number of neurons in each population
p.set_number_of_neurons_per_core(p.IF_curr_exp, nNeurons / 2)

cell_params_lif = {'cm': 0.25,
                   'i_offset': 0.0,
                   'tau_m': 20.0,
                   'tau_refrac': 2.0,
                   'tau_syn_E': 5.0,
                   'tau_syn_I': 5.0,
                   'v_reset': -70.0,
                   'v_rest': -65.0,
                   'v_thresh': -50.0
                   }

populations = list()
projections = list()

weight_to_spike = 2.0
delay = 17

loopConnections = list()
for i in range(0, nNeurons - 1):
    singleConnection = ((i, (i + 1) % nNeurons, weight_to_spike, delay))
    loopConnections.append(singleConnection)

injectionConnection = [(0, 0)]
injectionConnection2 = [(1, 1)]

populations.append(
    p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif), label='pop_1'))
populations.append(
    p.Population(nNeurons, p.IF_curr_exp(**cell_params_lif), label='pop_2'))
populations.append(
    p.Population(2, p.external_devices.SpikeInjector(), label='inputSpikes_1'))

projections.append(p.Projection(
    populations[0], populations[0], p.FromListConnector(loopConnections),
    p.StaticSynapse(weight=weight_to_spike, delay=delay)))
projections.append(p.Projection(
    populations[1], populations[1], p.FromListConnector(loopConnections),
    p.StaticSynapse(weight=weight_to_spike, delay=delay)))
projections.append(p.Projection(
    populations[2], populations[0], p.FromListConnector(injectionConnection),
    p.StaticSynapse(weight=weight_to_spike, delay=1)))
projections.append(p.Projection(
    populations[2], populations[1], p.FromListConnector(injectionConnection2),
    p.StaticSynapse(weight=weight_to_spike, delay=1)))

populations[0].record(['spikes'])
populations[1].record(['spikes'])

p.external_devices.activate_live_output_for(populations[0])
p.external_devices.activate_live_output_for(populations[1])

live_connection = p.external_devices.SpynnakerLiveSpikesConnection(
    receive_labels=['pop_1', 'pop_2'], send_labels=["inputSpikes_1"])


def receive_spikes_1(label, time, neuron_ids):
    print "Received spikes from population {}, neurons {} at time {}".format(
        label, neuron_ids, time)
    if (nNeurons - 1) in neuron_ids:
        print "Sending spike to neuron 1 of input"
        live_connection.send_spike("inputSpikes_1", 1)


def receive_spikes_2(label, time, neuron_ids):
    print "Received spikes from population {}, neurons {} at time {}".format(
        label, neuron_ids, time)
    if (nNeurons - 1) in neuron_ids:
        print "Sending spike to neuron 0 of input"
        live_connection.send_spike("inputSpikes_1", 0)


def send_spike(label, sender):
    time.sleep(0.01)
    print "Sending spike to neuron 0"
    sender.send_spike(label, 0)


live_connection.add_receive_callback('pop_1', receive_spikes_1)
live_connection.add_receive_callback("pop_2", receive_spikes_2)
live_connection.add_start_callback("inputSpikes_1", send_spike)

p.run(runtime)

# get data (could be done as one, but can be done bit by bit as well)
spikes_1 = populations[0].get_data('spikes')
spikes_2 = populations[1].get_data('spikes')

line_properties = [{'color': 'red', 'markersize': 2},
                   {'color': 'blue', 'markersize': 2}]

Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(spikes_1.segments[0].spiketrains,
          spikes_2.segments[0].spiketrains,
          yticks=True, line_properties=line_properties, xlim=(0, runtime)),
    title="Simple synfire chain example",
    annotations="Simulated with {}".format(p.name())
)
plt.show()

p.end()
