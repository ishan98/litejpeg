# Frontend wrapper
import math

from litex.gen import *
from litex.soc.interconnect.stream import *
from litex.soc.interconnect.stream_sim import *

from litejpeg.core.csc import RGB2YCbCr
from litejpeg.core.new_dct6 import DCT
from litejpeg.core.quantization import Quantization
from litejpeg.core.zigzag import ZigZag
from litejpeg.core.rle.rlemain import RLEmain
from litejpeg.core.huffman.huffmancore import HuffmanEncoder
from litejpeg.core.byte_stuffer.byteStuffer import ByteStuffer
from litejpeg.core.common import *

class frontendwrap(PipelinedActor, Module):
    def __init__(self, rgb_w=8, ycbcr_w=8, coef_w=8):

        self.submodules.streamer5 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.rlecore = RLEmain()
        self.submodules.logger5 = PacketLogger(
                                     EndpointDescription([("data", 21)]))
        self.submodules.streamer6 = PacketStreamer(
                                        EndpointDescription([("data",20)]))
        self.submodules.huffman = HuffmanEncoder()
        self.submodules.logger6 = PacketLogger(
                                      EndpointDescription([("data",9)]))
        self.submodules.streamer7 = PacketStreamer(
                                        EndpointDescription([("data",8)]))
        self.submodules.bytestuffer = ByteStuffer()
        self.submodules.logger7 = PacketLogger(
                                      EndpointDescription([("data",8)]))


        """self.submodules.streamer1 = PacketStreamer(
                                        EndpointDescription([("data",24)]))
        self.submodules.rgb2ycbcr = RGB2YCbCr()
        self.submodules.logger1 = PacketLogger(
                                      EndpointDescription([("data",8)]))
        self.submodules.streamer2 = PacketStreamer(
                                      EndpointDescription([("data", 8)]))
        self.submodules.dct = DCT()
        self.submodules.logger2 = PacketLogger(
                                      EndpointDescription([("data", 12)]))
        self.submodules.streamer3 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.quantization = Quantization()
        self.submodules.logger3 = PacketLogger(
                                     EndpointDescription([("data", 12)]))
        self.submodules.streamer4 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.zigzag = ZigZag()
        self.submodules.logger4 = PacketLogger(
                                     EndpointDescription([("data", 12)]))
        self.submodules.streamer5 = PacketStreamer(
                                       EndpointDescription([("data", 12)]))
        self.submodules.rlecore = RLEmain()
        self.submodules.logger5 = PacketLogger(
                                     EndpointDescription([("data", 21)]))
        self.submodules.streamer6 = PacketStreamer(
                                        EndpointDescription([("data",20)]))
        self.submodules.huffman = HuffmanEncoder()
        self.submodules.logger6 = PacketLogger(
                                      EndpointDescription([("data",9)]))
        self.submodules.streamer7 = PacketStreamer(
                                        EndpointDescription([("data",8)]))
        self.submodules.bytestuffer = ByteStuffer()
        self.submodules.logger7 = PacketLogger(
                                      EndpointDescription([("data",8)]))
"""


        # Connecting the zigzag module with the test bench.
        self.comb += [

            self.streamer5.source.connect(self.rlecore.sink),
            self.rlecore.source.connect(self.logger5.sink),

            self.streamer6.source.connect(self.huffman.sink),
            self.huffman.source.connect(self.logger6.sink),

            self.streamer7.source.connect(self.bytestuffer.sink),
            self.bytestuffer.source.connect(self.logger7.sink),

            #Record.connect(self.streamer1.source, self.rgb2ycbcr.sink, omit=["data"]),
            #self.rgb2ycbcr.sink.payload.r.eq(self.streamer1.source.data[16:24]),
            #self.rgb2ycbcr.sink.payload.g.eq(self.streamer1.source.data[8:16]),
            #self.rgb2ycbcr.sink.payload.b.eq(self.streamer1.source.data[0:8]),

            #Record.connect(self.rgb2ycbcr.source, self.logger1.sink, omit=["y","cb","cr"]),
            #self.logger1.sink.data.eq(self.rgb2ycbcr.source.y),

            #self.streamer2.source.connect(self.dct.sink),
            #self.dct.source.connect(self.logger2.sink),

            #self.streamer3.source.connect(self.quantization.sink),
            #self.quantization.source.connect(self.logger3.sink),

            #self.streamer4.source.connect(self.zigzag.sink),
            #self.zigzag.source.connect(self.logger4.sink),

            #self.streamer5.source.connect(self.rlecore.sink),
            #self.rlecore.source.connect(self.logger5.sink),

            #self.streamer6.source.connect(self.huffman.sink),
            #self.huffman.source.connect(self.logger6.sink),

            #self.streamer7.source.connect(self.bytestuffer.sink),
            #self.bytestuffer.source.connect(self.logger7.sink),

            #self.logger1.sink.connect(self.streamer2.source),
            #self.logger2.sink.connect(self.streamer3.source),
            #self.logger3.sink.connect(self.streamer4.source),
            #self.logger4.sink.connect(self.streamer5.source),
            self.logger5.sink.connect(self.streamer6.source),
            self.logger6.sink.connect(self.streamer7.source)

        ]
