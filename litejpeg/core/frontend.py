# Frontend wrapper
import math

from litex.gen import *
from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.csc import RGB2YCbCr
from litejpeg.core.common import *

class frontendwrap(PipelinedActor, Module):
    def __init__(self, rgb_w=8, ycbcr_w=8, coef_w=8):
        self.source = source = Endpoint(EndpointDescription([("data",24)])),
        self.sink = sink = Endpoint(EndpointDescription([("data",24)])),

        self.submodules.streamer = PacketStreamer(EndpointDescription([("data", 24)]))
        self.submodules.rgb2ycbcr = RGB2YCbCr()
        self.submodules.logger = PacketLogger(EndpointDescription([("data", 24)]))

        # Combining test bench with the RGB2YCbCr module.
        self.comb += [
        	Record.connect(self.streamer.source, self.rgb2ycbcr.sink, omit=["data"]),
            self.rgb2ycbcr.sink.payload.r.eq(self.streamer.source.data[16:24]),
            self.rgb2ycbcr.sink.payload.g.eq(self.streamer.source.data[8:16]),
            self.rgb2ycbcr.sink.payload.b.eq(self.streamer.source.data[0:8]),

            Record.connect(self.rgb2ycbcr.source, self.logger.sink, omit=["y", "cb", "cr"]),
            self.logger.sink.data[16:24].eq(self.rgb2ycbcr.source.y),
            self.logger.sink.data[8:16].eq(self.rgb2ycbcr.source.cb),
            self.logger.sink.data[0:8].eq(self.rgb2ycbcr.source.cr)
        ]
