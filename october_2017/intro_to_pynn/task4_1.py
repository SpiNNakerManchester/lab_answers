import spynnaker8 as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import random

simtime = 5000

# Write a network with a 1.0ms time step
sim.setup(timestep=1.0)

# consisting of two single-neuron populations
pre_pop = sim.Population(1, sim.IF_curr_exp(), label="Pre")
post_pop = sim.Population(1, sim.IF_curr_exp(), label="Post")

# connected with an STDP synapse using a spike pair rule
# and additive weight dependency, and initial weights of 0.
timing_rule = sim.SpikePairRule(tau_plus=20.0, tau_minus=20.0,
                                A_plus=0.5, A_minus=0.5)
weight_rule = sim.AdditiveWeightDependence(w_max=5.0, w_min=0.0)

stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=0.0, delay=5.0)
stdp_projection = sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                                 synapse_type=stdp_model)

# Stimulate each of the neurons with a spike source array with times of your
# choice, with the times for stimulating the first neuron being slightly
# before the times stimulating the second neuron (e.g.2ms or more),
# ensuring the times are far enough apart not to cause depression
# (compare the spacing in time with the tau_plus and tau_minus settings);
# note that a weight of 5.0 should be enough to force an IF_curr_exp neuron to
# fire with the default parameters.
# Add a few extra times at the end of the run for stimulating the first neuron.
spike = 0
spike_times1 = []
spike_times2 = []
while spike < simtime / 2:
    spike += random.randint(10, 30)
    spike_times1.append(spike)
    spike_times2.append(spike+random.randint(2, 5))
while spike < simtime:
    spike += random.randint(10, 30)
    spike_times1.append(spike)
print("spike_times1")
print(spike_times1)
print("spike_times2")
print(spike_times2)
input1 = sim.Population(1, sim.SpikeSourceArray(spike_times=spike_times1),
                        label="input1")
input2 = sim.Population(1, sim.SpikeSourceArray(spike_times=spike_times2),
                        label="input1")

sim.Projection(input1,  pre_pop,  sim.OneToOneConnector(),
               synapse_type=sim.StaticSynapse(weight=2.0))
sim.Projection(input2, post_pop, sim.OneToOneConnector(),
               synapse_type=sim.StaticSynapse(weight=2.0))

# Run the network for a number of milliseconds and
# extract the spike times of the neurons and the weights.

pre_pop.record("spikes")
post_pop.record("spikes")

pre_weights = stdp_projection.getWeights()

sim.run(simtime)

pre_neo = pre_pop.get_data(variables=["spikes"])
pre_spikes = pre_neo.segments[0].spiketrains

post_neo = post_pop.get_data(variables=["spikes"])
post_spikes = post_neo.segments[0].spiketrains

post_weights = stdp_projection.getWeights()

sim.end()

print(pre_weights)
print("pre_weights")
print(post_weights)
print("post_weights")

line_properties = [{'color': 'red'}, {'color': 'blue'}]

plot.Figure(
    # plot spikes
    plot.Panel(pre_spikes, post_spikes, yticks=True, xticks=True, markersize=5,
               xlim=(0, simtime), line_properties=line_properties),
    plot.Panel(pre_spikes, yticks=True, xticks=True, markersize=5,
               xlim=(0, simtime), color='red', data_labels=["pre"]),
    plot.Panel(post_spikes, yticks=True, xticks=True, markersize=5,
               xlim=(0, simtime), color='blue', data_labels=["post"]),
    title="Balanced Random Network Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
