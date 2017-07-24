# This is the module for testing the Huffman Encoder.

# !/usr/bin/env python3
from litex.gen import *

from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.huffman.huffman import Huffman

from common import *

# Testbanch for the Huffman module.

"""
Under this module a matrix containing 64 blocks is been sent as an
input to the Huffman and the output is been printed and compared
with the one from the reference modules.
In this way the result from the Huffman is been verified.
"""
class TB(Module):
    def __init__(self):
        # Making pipeline and the getting the Huffman module.
        """
        Streamer : It will pass the input to the Huffman.
                   The data is a 20 bit number in the matrix.
                   Streamer[0:12] = Amplitude
                   Streamer[12:16] = Size of the Amplitude
                   Streamer[16:20] = Runlength

        Logger : It will get the output to the TestBench.
                 The output of the testBench is the variable length values of the
                 ranging from 0,8 or 16 bits depending upon the encoding done
                 as per the huffman tables.
        """
        self.submodules.streamer = PacketStreamer(EndpointDescription([("data", 20)]))
        self.submodules.huffman = Huffman()
        self.submodules.logger = PacketLogger(EndpointDescription([("data", 16)]))

        # Connecting TestBench with the RLEcore module.
        self.comb += [
            self.streamer.source.connect(self.huffman.sink),
            self.huffman.source.connect(self.logger.sink)
        ]


def main_generator(dut):

    # Results from the implemented module.
    model2 = Huffman()
    packet = Packet(model2.red_pixels_1)
    for i in range(1):
        dut.streamer.send(packet)
        yield from dut.logger.receive()
        print("\n")
        print("Output of the RLE module:")
        model2.setdata(dut.logger.packet)

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