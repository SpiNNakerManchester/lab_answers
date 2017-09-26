import spynnaker8 as sim
import spynnaker8.spynakker_plotting as splot
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
from pyNN.random import RandomDistribution, NumpyRNG

# Remove random effect for testing
# Set to None to randomize
rng = NumpyRNG(seed=1)

# Choose the number of neurons to be simulated in the network.
n_neurons = 100
n_exc = int(round(n_neurons * 0.8))
n_inh = int(round(n_neurons * 0.2))
simtime = 5000

# Set up the simulation to use 0.1ms timesteps.
sim.setup(timestep=0.1)

# Create an excitatory population with 80% of the neurons and
# an inhibitory population with 20% of the neurons.
pop_exc = sim.Population(n_exc, sim.IF_curr_exp(), label="Excitatory")
pop_inh = sim.Population(n_inh, sim.IF_curr_exp(), label="Inhibitory")

# Create excitatory poisson stimulation population with 80%
#    of the neurons and
# an inhibitory poisson stimulation population with 20% of the neurons,
#  both with a rate of 1000Hz
# TODO RATE?
if rng is None:
    seed = None
else:
    seed = int(rng.next()*1000)
stim_exc = sim.Population(n_exc, sim.SpikeSourcePoisson(rate=1000.0, seed=seed),
                          label="Stim_Exc")
if rng is None:
    seed = None
else:
    seed = int(rng.next()*1000)
stim_inh = sim.Population(n_inh, sim.SpikeSourcePoisson(rate=1000.0, seed=int(rng.next()*1000)),
                          label="Stim_Inh")

# Create a one-to-one excitatory connection
# from the excitatory poisson stimulation population
# to the excitatory population with a weight of 0.1nA and a delay of 1.0ms
# TODO values
ex_proj = sim.Projection(
    stim_exc, pop_exc, sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=0.1, delay=1.0),
    receptor_type="excitatory")

# Create a similar excitatory connection
# from the inhibitory poisson stimulation population
# to the inhibitory population.
in_proj = sim.Projection(
    stim_inh, pop_inh, sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=0.1, delay=1.0),
    receptor_type="excitatory")

# Create an excitatory connection from the excitatory population
# to the inhibitory population
# with a fixed probability of connection of 0.1,
# and using a normal distribution of weights with a mean of 0.1 (mu)
#   and standard deviation of 0.1 (sigma)
#   (remember to add a boundary to make the weights positive)
# and a normal distribution of delays with a mean of 1.5 (mu)
#   and standard deviation of 0.75 (sigma)
#   (remember to add a boundary to keep the delays
#       within the allowed range on SpiNNaker).
# TODO  Values
rd_exc_weights = RandomDistribution('normal_clipped', mu=0.1, sigma=0.1, low=0,
                                    high=100, rng=rng)
rd_exc_delays = RandomDistribution('normal_clipped', mu=1.5, sigma=0.75, low=1,
                                   high=15, rng=rng)
ex_in_proj = sim.Projection(
    pop_exc, pop_inh, sim.FixedProbabilityConnector(0.1, rng=rng),
    synapse_type=sim.StaticSynapse(weight=rd_exc_weights, delay=rd_exc_delays),
    receptor_type="excitatory")

# Create a similar connection between the excitatory population and itself.
ex_ex_proj = sim.Projection(
    pop_exc, pop_exc, sim.FixedProbabilityConnector(0.1, rng=rng),
    synapse_type=sim.StaticSynapse(weight=rd_exc_weights, delay=rd_exc_delays),
    receptor_type="excitatory")


# Create an inhibitory connection from the inhibitory population to the
# excitatory population with a fixed probability of connection of 0.1,
# and using a normal distribution of weights with a
# mean of -0.4 and standard deviation of 0.1
# (remember to add a boundary to make the weights negative)
# and a normal distribution of delays with a mean of 0.75 and
# standard deviation of 0.375 (remember to add a boundary to keep the delays
# within the allowed range on SpiNNaker).
rd_inh_weights = RandomDistribution('normal_clipped', mu=-0.4, sigma=0.1,
                                    low=-100,  high=0, rng=rng)
rd_inh_delays = RandomDistribution('normal_clipped', mu=0.75, sigma=0.375,
                                   low=1, high=15, rng=rng)
in_ex_proj = sim.Projection(
    pop_inh, pop_exc, sim.FixedProbabilityConnector(0.1, rng=rng),
    synapse_type=sim.StaticSynapse(weight=rd_inh_weights, delay=rd_inh_delays),
    receptor_type="inhibitory")

# Create a similar connection between the inhibitory population and itself.
in_in_proj = sim.Projection(
    pop_inh, pop_inh, sim.FixedProbabilityConnector(0.1, rng=rng),
    synapse_type=sim.StaticSynapse(weight=rd_inh_weights, delay=rd_inh_delays),
    receptor_type="inhibitory")

# Initialize the membrane voltages of the excitatory and inhibitory populations
# to a uniform random number between -65.0 and -55.0.
pop_exc.initialize(
    v=RandomDistribution("uniform", parameters_pos=[-65.0, -55.0], rng=rng))
pop_inh.initialize(
    v=RandomDistribution("uniform", parameters_pos=[-65.0, -55.0], rng=rng))

# Record the spikes from the excitatory population.
pop_exc.record(["spikes", "v"])
pop_inh.record("spikes")

# Run the simulation for 1 or more seconds.
sim.run(simtime)


# Retrieve and plot the spikes.
neo_exc = pop_exc.get_data(variables=["spikes", "v"])
spikes_exc = neo_exc.segments[0].spiketrains
print "spikes_exc"
for i in range(n_exc):
    for spike in spikes_exc[i]:
        print i, spike
v_exc = neo_exc.segments[0].filter(name='v')[0]
neo_inh = pop_inh.get_data(variables=["spikes"])
spikes_inh = neo_inh.segments[0].spiketrains
print "spikes_inh"
for i in range(n_inh):
    for spike in spikes_inh[i]:
        print i, spike

plot.Figure(
    # plot spikes
    splot.SpynakkerPanel(spikes_exc, yticks=True, markersize=5,
                         xlim=(0, simtime), data_labels=[pop_exc.label]),
    splot.SpynakkerPanel(spikes_inh, yticks=True, markersize=5,
                         xlim=(0, simtime), data_labels=[pop_inh.label]),
    splot.SpynakkerPanel(v_exc, ylabel="Pop[0] Membrane potential (mV)",
                         data_labels=[pop_exc.label], xticks=True, yticks=True,
                         xlim=(0, simtime)),
    title="Balanced Random Cortel-like",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
