# This is the module for testing the ByteStuffer.

# !/usr/bin/env python3
from litex.gen import *

from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.byte_stuffer.byteStuffer import ByteStuffer

from common import *

# Testbanch for the ByteStuffer module.
"""
Under this module a matrix containing 64 blocks is been sent as an
input to the ByteStuffer and the output is been printed and compared
with the one from the reference modules.
In this way the result from the ByteStuffer is been verified.
"""
class TB(Module):
    def __init__(self):
        # Making pipeline and the getting the ByteStuffer module.
        """
        Streamer : It will pass the input to the ByteStuffer.
                   The data is a 8 bit number in the matrix.
                   Streamer[0:8] = Sink

        Logger : It will get the output to the TestBench.
                 The output of the ByteStuffer is of 8 bits
                 after passing through mux deciding wheather it is of the
                 form of 0xFF or other.
                 Logger[0:8] = Output of the ByteStuffer
        """
        self.submodules.streamer = PacketStreamer(EndpointDescription([("data", 8)]))
        self.submodules.bytestuffer = ByteStuffer()
        self.submodules.logger = PacketLogger(EndpointDescription([("data", 8)]))

        # Connecting TestBench with the Huffman Encoder module.
        self.comb += [
            self.streamer.source.connect(self.bytestuffer.sink),
            self.bytestuffer.source.connect(self.logger.sink)
        ]


def main_generator(dut):

    # Results from the implemented module.
    model = BStuffer()
    packet = Packet(model.stuffer_in)
    for i in range(1):
        dut.streamer.send(packet)
        yield from dut.logger.receive()
        print(dut.logger.packet)


# Going through the main module
if __name__ == "__main__":
    tb = TB()
    generators = {"sys" : [main_generator(tb)]}
    generators = {
        "sys" :   [main_generator(tb),
                   tb.streamer.generator(),
                   tb.logger.generator()]
    }
    clocks = {"sys": 10}
    run_simulation(tb, generators, clocks, vcd_name="sim.vcd")
