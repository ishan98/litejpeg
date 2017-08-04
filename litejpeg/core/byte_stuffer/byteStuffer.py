"""
 Bytestuffer Module
 This contains the top module for the ByteStuffer
 """

# Import libraries
from litex.gen import *
from litex.soc.interconnect.stream import *

from litejpeg.core.common import *
"""
Byte Stuffer:
-------------
The main function of the ByteStuffer is to add zeros Byte after the
incounter of any 0xFF as an input from the other blocks.
Input : 8 bits
Output: 8 bits
"""

# To synchronize the data with the latency of the module.
datapath_latency = 1

# Insert an extra clock.
@CEInserter()

class ByteStufferDatapath(Module):
    """
    The main function of this class is to add datapath to the
    ByteStuffer module.

    Parameters:
    -----------
    sink : 8 bits
           input the byte into the datapath.
    source : 8 bits
             output the byte to the main module.
    ready_data_write : 1 bit
                       Check wheather the datapath is ready
                       to process new data.
    ready_data_read : 1 bit
                      Check wheather the data in the source
                      is valid or not.
    """
    def __init__(self):

        self.sink = sink = Record(block_layout(8))
        self.source = source = Record(block_layout(8))

        self.ready_data_read = Signal()
        self.ready_data_write = Signal()

        # MUX to decide wheather the recieved data is '0xFF' or not.
        # If 'YES' than make the output to be equal to output
        # and fix the next output to be 0.
        # Else put the output= input and recieve the next data.
        self.sync += [
        If(self.sink.data == 0xFF,
           self.source.data.eq(0xFF),
           self.ready_data_write.eq(0),
           self.ready_data_read.eq(1)
        ).Else(
           self.source.data.eq(self.sink.data),
           self.ready_data_write.eq(1),
           self.ready_data_read.eq(1)
        )
        ]

        # Adding zero as the output on recieving 0xFF and get ready
        # for next input.
        self.sync += [
        If(~self.ready_data_write,
            self.source.data.eq(0x00),
            self.ready_data_write.eq(1),
            self.ready_data_read.eq(0)
          )
        ]



class ByteStuffer(PipelinedActor, Module):
    """
    This class is made to take input from other modules or the test bench
    and give the data out to the datapath whenever the datapath is ready and
    also recieve it from the same after the ready_data_write is equal to 1.
    Paramaters :
    sink : 8 bits
           recieve inputs from the other modules.
    source : 8 bits
             write output to other modules.
    ready_data_read : 1 bit
                      decide wheather the given data is valid or not.
    ready_data_write: 1 bit
                      decide wheather the module is ready to take input_data.
    """
    def __init__(self):
        # Connecting ByteStuffer to the other modules.
        self.sink = sink = stream.Endpoint(EndpointDescription(block_layout(8)))
        self.source = source = stream.Endpoint(EndpointDescription(block_layout(9)))

        PipelinedActor.__init__(self,datapath_latency)
        self.latency = datapath_latency

        self.ready_data_write = Signal()
        self.ready_data_read = Signal()

        # Connecting main module to the datapath.
        self.submodules.datapath = ByteStufferDatapath()
        self.comb += self.datapath.ce.eq(self.pipe_ce)

        write_sel = Signal()
        write_swap = Signal()
        read_sel = Signal(reset=1)
        read_swap = Signal()

        # To swap the read and write select whenever required.
        self.sync += [
            If(write_swap,
                write_sel.eq(~write_sel)
            ),
            If(read_swap,
                read_sel.eq(~read_sel)
            )
        ]

        # write path

        # To start the write_count back to 0.
        write_clear = Signal()
        # To increment the write_count.
        write_inc = Signal()
        # To keep track over which value of the matrix is under process.
        write_count = Signal(6)

        # For tracking the data adress.
        self.sync += \
            If(write_clear,
                write_count.eq(0)
            ).Elif(write_inc,
                write_count.eq(write_count + 1)
            )

        # To combine the ByteStuffer datapath into the main module.
        self.comb += [
            self.ready_data_write.eq(self.datapath.ready_data_write),
            self.datapath.sink.data.eq(sink.data)
        ]



        """
        GET_RESET.

        Depending on the value of the read_sel and write_sel decide wheather the
        next state will be either read or write.
        Will clear the value of ``write_count`` to be 0.
        """
        self.submodules.write_fsm = write_fsm = FSM(reset_state="GET_RESET")
        write_fsm.act("GET_RESET",
            write_clear.eq(1),
            self.ready_data_write.eq(1),
            If(write_sel != read_sel,
                NextState("WRITE_INPUT")
            )
        )

        """
        WRITE_INPUT State

        Will increament the value of the write_count at every positive edge of the
        clock cycle till 63 and write the data into the memory as per the data
        from the ``sink.data`` and when the value reaches 63 the state again changes to
        that of the IDLE state.
        """
        write_fsm.act("WRITE_INPUT",
        If(self.ready_data_write,
            sink.ready.eq(1),
            If(sink.valid,
                If(write_count == 63,
                    write_swap.eq(1),
                    NextState("GET_RESET")
                ).Else(
                    write_inc.eq(1)
                )
            )
        ).Else(
            sink.ready.eq(0),
            write_inc.eq(0)
        )
        )

        # read path

        # Intialising the values.
        read_clear = Signal()
        read_inc = Signal()
        read_count = Signal(6)

        # For keeping track of the adress by using the read_count.
        self.sync += \
            If(read_clear,
                read_count.eq(0)
            ).Elif(read_inc,
                read_count.eq(read_count + 1)
            )

        # Reading the input from the Datapath only when the output data is valid.
        self.comb += [
            self.ready_data_read.eq(self.datapath.ready_data_read),
            If(self.datapath.ready_data_read,
                source.data.eq(self.datapath.source.data)
                )
        ]

        #GET_RESET state
        self.submodules.read_fsm = read_fsm = FSM(reset_state="GET_RESET")
        read_fsm.act("GET_RESET",
            read_clear.eq(1),
            self.ready_data_read.eq(1),
            If(read_sel == write_sel,
                read_swap.eq(1),
                NextState("READ_OUTPUT")
            )
        )
        """
        READ_INPUT state

        Will increament the value of the read_count at every positive edge of the
        clock cycle till 63 and read the data from the memory, giving it to the
        ``source.data`` as input and when the value reaches 63 the state again changes to
        that of the IDLE state.
        """
        read_fsm.act("READ_OUTPUT",
        If(self.ready_data_read,
            source.valid.eq(1),
            source.last.eq(read_count == 63),
            If(source.ready,
            	read_inc.eq(1),
                If(source.last,
                    NextState("GET_RESET")
                )
            )
        ).Else(
            source.valid.eq(0),
            read_inc.eq(0)
           )
        )
