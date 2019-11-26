import pyNN.spiNNaker as p
from spynnaker8.utilities import DataHolder
from pacman.model.routing_info.base_key_and_mask import BaseKeyAndMask
from pacman.model.constraints.key_allocator_constraints \
    import FixedKeyAndMaskConstraint
from spinn_front_end_common.abstract_models import (
    AbstractProvidesOutgoingPartitionConstraints,
    ApplicationSpiNNakerLinkVertex)


class MySpiNNakerLinkDevice(
        ApplicationSpiNNakerLinkVertex,
        AbstractProvidesOutgoingPartitionConstraints):

    def __init__(
            self, n_neurons, spinnaker_link_id, label=None):
        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_neurons, spinnaker_link_id, label=label)

    def get_outgoing_partition_constraints(self, partition):
        return [FixedKeyAndMaskConstraint([
            BaseKeyAndMask(0x12340000, 0xFFFF0000)])]


class MySpiNNakerLinkDeviceDataHolder(DataHolder):

    def __init__(self, spinnaker_link_id, label=None):
        DataHolder.__init__(
            self, {"spinnaker_link_id": spinnaker_link_id, "label": label})

    @staticmethod
    def build_model():
        return MySpiNNakerLinkDevice


p.setup(1.0)

pop = p.Population(1, p.IF_curr_exp())
device = p.Population(1, MySpiNNakerLinkDeviceDataHolder(spinnaker_link_id=0))

p.Projection(device, pop, p.OneToOneConnector(), p.StaticSynapse(weight=1.0))

p.run(100)

p.end()
