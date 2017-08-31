.. JPEG encoder documentation documentation master file, created by
   sphinx-quickstart on Wed Aug 30 12:33:03 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to JPEG encoder's documentation!
======================================================
This contains all the necessary information regarding the Top level JPEG design and the various submodules present in the same.

Submodules
----------
The encoder consist of several submodules which includes as follows:
* RGB2YCbCr module
* DCT2D module
* Quantization module
* Zigzag module
* RLE module
* Huffman encoder module.
* ByteStuffer module.

Top Level JPEG datapath
-----------------------
The JPEG encoder implemention is based on the Ready-Valid Handshake protocol in which small FSM's are implemented for each of the submodules required for creating the JPEG encoder. The prior FSM will generate a Valid signal to the latter submodule regarding the input data to be valid and than when the latter is ready to take the data, it generates a ready signal and than the data is been transferred within the two modules.

Submodules:

.. toctree::
   :maxdepth: 2
   
   RGB2YCbCr<subblocks/rgb2ycbcr.rst>
   DCT2D<subblocks/dct2d.rst>
   Quantizer<subblocks/quantizer.rst>
   Zigzag<subblocks/zigzag.rst>
   RLE<subblocks/rle.rst>
   Huffman<subblocks/huffman.rst>
   ByteStuffer<subblocks/bytestuffer.rst>

Test Files:

.. toctree::
   :maxdepth: 2
   
   RGB2YCbCr Test<subblocks/rgb2ycbcr_test.rst>
   DCT2D Test<subblocks/dct2d_test.rst>
   Quantizer Test<subblocks/quantizer_test.rst>
   Zigzag Test<subblocks/zigzag_test.rst>
   RLE Test<subblocks/rle_test.rst>
   Huffman Test<subblocks/huffman_test.rst>
   ByteStuffer Test<subblocks/bytestuffer_test.rst>


   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
