# This is the module for testing the frontend.

# !/usr/bin/env python3
from litex.gen import *

from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.common import *
from litejpeg.core.frontend import frontendwrap
from litejpeg.core.csc import rgb2ycbcr_coefs

from common import *

class TB(Module):
    def __init__(self):
        # Making pipeline for getting Frontend module.
        self.submodules.streamer = PacketStreamer(EndpointDescription([("data", 12)]))
        self.submodules.front = frontendwrap()
        self.submodules.logger = PacketLogger(EndpointDescription([("data", 21)]))

        # Combining test bench with the Frontend module.
        self.comb += [
            Record.connect(self.streamer.source, self.front.streamer5.source, omit=["data"]),
            self.front.streamer5.source.data.eq(self.streamer.source.data),

            Record.connect(self.front.logger7.sink, self.logger.sink, omit=["data"]),
            self.logger.sink.data.eq(self.front.logger7.sink.data)
            ]


def main_generator(dut):

    # convert image using rgb2ycbcr implementation
    model = Quantizer()
    raw_image = RAWImage(rgb2ycbcr_coefs(8), "lena.png", 64)
    raw_image.pack_rgb()
    packet = Packet(raw_image.data)
    print(packet)
    dut.streamer.send(packet)
    yield from dut.logger.receive()
    print(dut.logger.packet)
    #model.setdata(dut.logger.packet)

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
