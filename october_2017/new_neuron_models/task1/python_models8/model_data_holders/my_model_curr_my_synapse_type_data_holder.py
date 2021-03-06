# main interface to use the spynnaker related tools.
# ALL MODELS MUST INHERIT FROM THIS
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex
from spynnaker8.utilities import DataHolder
from python_models8.neuron.builds.my_model_curr_my_synapse_type \
    import MyModelCurrMySynapseTypeBase


class MyModelCurrMySynapseTypeDataHolder(DataHolder):
    def __init__(
            self, spikes_per_second=(
                AbstractPopulationVertex.non_pynn_default_parameters[
                    'spikes_per_second']),
            ring_buffer_sigma=(
                AbstractPopulationVertex.non_pynn_default_parameters[
                    'ring_buffer_sigma']),
            incoming_spike_buffer_size=(
                AbstractPopulationVertex.non_pynn_default_parameters[
                    'incoming_spike_buffer_size']),
            constraints=AbstractPopulationVertex.non_pynn_default_parameters[
                'constraints'],
            label=AbstractPopulationVertex.non_pynn_default_parameters[
                'label'],
            v_init=MyModelCurrMySynapseTypeBase.initialize_parameters[
                'v_init'],
            v_thresh=MyModelCurrMySynapseTypeBase.default_parameters[
                'v_thresh'],
            my_ex_synapse_parameter=(
                MyModelCurrMySynapseTypeBase.default_parameters[
                    'my_ex_synapse_parameter']),
            my_in_synapse_parameter=(
                MyModelCurrMySynapseTypeBase.default_parameters[
                    'my_in_synapse_parameter']),
            my_exc_init=MyModelCurrMySynapseTypeBase.default_parameters[
                'my_exc_init'],
            my_inh_init=MyModelCurrMySynapseTypeBase.default_parameters[
                'my_inh_init'],
            my_parameter=MyModelCurrMySynapseTypeBase.default_parameters[
                'my_parameter'],
            v_rest=MyModelCurrMySynapseTypeBase.default_parameters[
                'v_rest'],
            decay=MyModelCurrMySynapseTypeBase.default_parameters[
                'decay'],
            i_offset=MyModelCurrMySynapseTypeBase.default_parameters[
                'i_offset']):
        DataHolder.__init__(
            self, {
                'spikes_per_second': spikes_per_second,
                'ring_buffer_sigma': ring_buffer_sigma,
                'incoming_spike_buffer_size': incoming_spike_buffer_size,
                'constraints': constraints,
                'label': label,
                'v_thresh': v_thresh,
                'my_ex_synapse_parameter': my_ex_synapse_parameter,
                'my_in_synapse_parameter': my_in_synapse_parameter,
                'my_exc_init': my_exc_init,
                'my_inh_init': my_inh_init,
                'i_offset': i_offset,
                'v_rest': v_rest, 'decay': decay,
                'my_parameter': my_parameter, 'v_init': v_init})

    @staticmethod
    def build_model():
        return MyModelCurrMySynapseTypeBase
