import geoio
import os
import collections
from glob import glob
from shutil import copyfile

from datetime import date


DG_SATID_TO_ENVI = {
    'WV01': 'WorldView-1',
    'WV02': 'WorldView-2',
    'WV03': 'WORLDVIEW-3',
    'IK01': 'IKONOS',
    'QB02': 'QuickBird',
    'GE01': 'GeoEye-1'
}

DG_WAVELENGTH_UNITS = 'nm'

def create_hdr(aop_path, output_port_path, debug="no", description=None, **kwargs):
    logit = kwargs.get('logger')
    #aop_path is assumed to be a path to the .tif file of an AOP image product
    filename = os.path.split(aop_path)[1]
    new_filename = '%s.hdr' % os.path.splitext(filename)[0]

    logit.debug('Search Pattern: %s' % ('%s.*' % os.path.splitext(aop_path)[0]))
    logit.debug('Input Files %s' % glob('%s.*' % os.path.splitext(aop_path)[0]))
    # Copy input files to output
    for filename in glob('%s.*' % os.path.splitext(aop_path)[0]):
        dest = os.path.join(output_port_path, os.path.split(filename)[1])
        copyfile(filename, dest)
        logit.debug('%s -> %s' % (filename, dest))

    #create empty hdr file
    hdr_file = open(os.path.join(output_port_path, new_filename), "w+")
    logit.debug('New log file: %s' % hdr_file)

    # Add fixed values hdr line
    hdr_file.write('ENVI\n')

    #open image in geoio
    img = geoio.DGImage(aop_path)

    logit.debug('Image Summary: %s' % img.print_img_summary)

    #create ordered dictto have some contraol over writing order
    envi_dict = collections.OrderedDict()
    #add elements to the ODict
    envi_dict['description'] = '{Creating ENVI hdr file from AOP data [%s]}'
    envi_dict['sensor type'] = DG_SATID_TO_ENVI[img.meta.satid]
    envi_dict['lines'] = str(img.meta.shape[1])
    envi_dict['samples'] = str(img.meta.shape[2])
    envi_dict['bands'] = str(img.meta.shape[0])
    envi_dict['band names'] = '{%s}' % ', '.join(str(e) for e in img.meta.band_names)
    envi_dict['wavelength'] = '{%s}' % ', '.join(str(e) for e in img.meta.band_centers)
    envi_dict['wavelength units'] = DG_WAVELENGTH_UNITS

    for entry, value in envi_dict.iteritems():
        #iterate through elements to write them out to file
        hdr_file.write('%s = %s\n' % (entry, value))

    logit.debug('Finished writing HDR file.')
    #close file
    hdr_file.close()
