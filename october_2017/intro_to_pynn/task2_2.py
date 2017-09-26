import spynnaker8 as sim
import spynnaker8.spynakker_plotting as splot
import pyNN.utility.plotting as plot
from pyNN.random import RandomDistribution
import matplotlib.pyplot as plt

simtime = 2000
n_neurons = 7
weight_to_spike = 5
delay = 5

sim.setup(timestep=1.0)

input = sim.Population(1, sim.SpikeSourceArray(spike_times=[[0], [1]]),
                       label="input")
pop = sim.Population(n_neurons, sim.IF_curr_exp(tau_syn_E=5), label="pop")

loop_conns = list()
for i in range(0, n_neurons - 1):
    single_connection = (i, i + 1)
    loop_conns.append(single_connection)
single_connection = (n_neurons - 1, 0)
loop_conns.append(single_connection)
print loop_conns

rd_delays = RandomDistribution('normal', (1, 15))

input_proj = sim.Projection(
    input, pop, sim.OneToOneConnector(),
    synapse_type=sim.StaticSynapse(weight=5, delay=2))
loop_proj = sim.Projection(
    pop, pop, sim.FromListConnector(loop_conns),
    synapse_type=sim.StaticSynapse(weight=5, delay=rd_delays))

pop.record(["spikes", "v"])
sim.run(simtime)

s_neo = pop.get_data(variables=["spikes"])
spikes = s_neo.segments[0].spiketrains
print spikes
v_neo = pop.get_data(variables=["v"])
v = v_neo.segments[0].filter(name='v')[0]
print v
print "shape"
print v.shape

sim.end()

plot.Figure(
    splot.SpynakkerPanel(
        v, ylabel="Pop[0] Membrane potential (mV)",
        data_labels=[pop.label], xticks=True, yticks=True, xlim=(0, simtime)),
    plot.Panel(
        v, ylabel="Pop[0] Membrane potential (mV)", data_labels=[pop.label],
        xticks=True, yticks=True, xlim=(0, simtime)),
    # plot spikes
    splot.SpynakkerPanel(spikes, yticks=True, xticks=True, markersize=5,
                         xlim=(0, simtime)),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
