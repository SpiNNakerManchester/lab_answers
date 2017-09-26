import spynnaker8 as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

simtime = 500
n_neurons = 100

# Set up the simulation to use a 1ms time step.
sim.setup(timestep=1)

# Create a population of 100 presynaptic neurons.
pre_pop = sim.Population(n_neurons, sim.IF_curr_exp(), label="presynaptic")

# Create a spike source array population of 100 sources connected to the
# presynaptic population.
# Set the spikes in the arrays so that each spikes twice 200ms apart,
# and that the first spike for each is 1ms after the first spike of the last
# e.g. [[0, 200], [1, 201], ...]
# (hint: you can do this with a list comprehension).
spike_times = [[x+y for x in [0, 200]] for y in range(n_neurons)]
print spike_times
pre_input = sim.Population(
    n_neurons, sim.SpikeSourceArray(spike_times=spike_times),
    label="pre input")
sim.Projection(pre_input,  pre_pop,  sim.OneToOneConnector(),
               synapse_type=sim.StaticSynapse(weight=5.0))

# Create a population of 100 postsynaptic neurons.
post_pop = sim.Population(n_neurons, sim.IF_curr_exp(), label="postsynaptic")
# Create a spike source array connected to the postsynaptic neurons all
# spiking at 50ms.
post_input = sim.Population(n_neurons, sim.SpikeSourceArray(spike_times=[50]),
                            label="pre input")
sim.Projection(post_input,  post_pop,  sim.OneToOneConnector(),
               synapse_type=sim.StaticSynapse(weight=5.0))

# Connect the presynaptic population to the postsynaptic population with an
# STDP projection with an initial weight of 0.5 and a maximum of 1
# and minimum of 0.
timing_rule = sim.SpikePairRule(tau_plus=20.0, tau_minus=20.0,
                                A_plus=0.5, A_minus=0.5)
weight_rule = sim.AdditiveWeightDependence(w_max=1, w_min=0.0)

stdp_model = sim.STDPMechanism(timing_dependence=timing_rule,
                               weight_dependence=weight_rule,
                               weight=0.5)
stdp_projection = sim.Projection(pre_pop, post_pop, sim.OneToOneConnector(),
                                 synapse_type=stdp_model)

# Record the presynaptic and postsynaptic populations.
pre_pop.record("spikes")
post_pop.record("spikes")

# Run the simulation for long enough for all spikes to occur,
# and get the weights from the STDP projection.
pre_weights = stdp_projection.getWeights()

sim.run(simtime)

post_weights = stdp_projection.getWeights()

print pre_weights
print "pre_weights"
print post_weights
print "post_weights"

# Draw a graph of the weight changes from the initial weight value against the
# difference in presynaptic and postsynaptic neurons
# (hint: the presynaptic neurons should spike twice but the postsynaptic
# should only spike once;
# you are looking for the first spike from each presynaptic neuron).
delta_weights = [post_weights[i] - pre_weights[i] for i in range(n_neurons)]

delta_times = [spike_times[i][0] - 50 for i in range(n_neurons)]

plt.plot(delta_times, delta_weights, ".")
plt.xlabel("Delta Times")
plt.ylabel("Delta Weights")
plt.axis([min(delta_times)-0.1, max(delta_times)+0.1,
          min(delta_weights)-0.1, max(delta_weights)+0.1])
plt.show()

# test
pre_neo = pre_pop.get_data(variables=["spikes"])
pre_spikes = pre_neo.segments[0].spiketrains
print "pre_spikes"
print pre_spikes

post_neo = post_pop.get_data(variables=["spikes"])
post_spikes = post_neo.segments[0].spiketrains
print "post_spikes"
print post_spikes


sim.end()

print pre_weights
print "pre_weights"
print post_weights
print "post_weights"

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
