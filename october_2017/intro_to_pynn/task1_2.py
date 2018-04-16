import spynnaker8 as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

simtime = 20

sim.setup(timestep=1.0)

pop_1 = sim.Population(2, sim.IF_curr_exp(tau_syn_E=1), label="pop_1")
input = sim.Population(2, sim.SpikeSourceArray(spike_times=[[0], [1]]),
                       label="input")
input_proj = sim.Projection(input, pop_1, sim.OneToOneConnector(),
                            synapse_type=sim.StaticSynapse(weight=5, delay=2))
pop_1.record(["spikes", "v"])

sim.run(simtime)

neo = pop_1.get_data(variables=["spikes", "v"])
spikes = neo.segments[0].spiketrains
print(spikes)
v = neo.segments[0].filter(name='v')[0]
print(v)

sim.end()

plot.Figure(
    plot.Panel(v, ylabel="Pop[0] Membrane potential (mV)",
               data_labels=[pop_1.label], xticks=True, yticks=True,
               xlim=(0, simtime)),
    # plot spikes (if any)
    plot.Panel(spikes, yticks=True, xticks=True, markersize=5,
               xlim=(0, simtime)),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
