# aop-hdr-creation
Will Cadell (will@sparkgeo.com)

A python function to create an ENVI .hdr file form DigitalGlobe AOP data using geoio

Inside "aop_to_envi_hdr.py" is a function "create_hdr" which creates an ENVI hdr file from data provided in DG metadata 
files which geoio can read. 

This function is expecting a .tif file as typical output from the DigitalGlobe AOP process.

The description can be provided as a way to pipe in more appropriate text.

# Example use

2envi.py is a commandline tool which shows an example of how to use aop_to_envi_hdr

$python 2envi.py -a ../imagery/055137665010_01_assembly.tif
