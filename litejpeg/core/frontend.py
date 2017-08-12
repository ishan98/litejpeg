# Frontend wrapper
import math

from litex.gen import *
from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.csc import RGB2YCbCr
from litejpeg.core.quantization import Quantization
from litejpeg.core.zigzag import ZigZag
from litejpeg.core.common import *

class frontendwrap(PipelinedActor, Module):
    def __init__(self, rgb_w=8, ycbcr_w=8, coef_w=8):

        self.submodules.streamer1 = PacketStreamer(
                                        EndpointDescription([("data",24)]))
        self.submodules.rgb2ycbcr = RGB2YCbCr()
        self.submodules.logger1 = PacketLogger(
                                      EndpointDescription([("data",8)]))
        self.submodules.streamer2 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.quantization = Quantization()
        self.submodules.logger2 = PacketLogger(
                                     EndpointDescription([("data", 12)]))
        self.submodules.streamer3 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.zigzag = ZigZag()
        self.submodules.logger3 = PacketLogger(
                                     EndpointDescription([("data", 12)]))

        # Connecting the zigzag module with the test bench.
        self.comb += [

            Record.connect(self.streamer1.source, self.rgb2ycbcr.sink, omit=["data"]),
            self.rgb2ycbcr.sink.payload.r.eq(self.streamer1.source.data[16:24]),
            self.rgb2ycbcr.sink.payload.g.eq(self.streamer1.source.data[8:16]),
            self.rgb2ycbcr.sink.payload.b.eq(self.streamer1.source.data[0:8]),

            Record.connect(self.rgb2ycbcr.source, self.logger1.sink, omit=["y","cb","cr"]),
            self.logger1.sink.data.eq(self.rgb2ycbcr.source.y),

            self.streamer2.source.connect(self.quantization.sink),
            self.quantization.source.connect(self.logger2.sink),

            self.streamer3.source.connect(self.zigzag.sink),
            self.zigzag.source.connect(self.logger3.sink),

            self.logger1.sink.connect(self.streamer2.source),
            self.logger2.sink.connect(self.streamer3.source)
        ]
