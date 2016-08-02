import geoio
import os
import collections
from glob import glob
from shutil import copyfile

RGB_BANDS = ['R', 'G', 'B']

DG_SATID_TO_ENVI = {
    'WV01': 'WorldView-1',
    'WV02': 'WorldView-2',
    'WV03': 'WORLDVIEW-3',
    'IK01': 'IKONOS',
    'QB02': 'QuickBird',
    'GE01': 'GeoEye-1'
}

DG_WAVELENGTH_UNITS = 'nm'

def create_hdr(img_path, output_port_path, **kwargs):
    logit = kwargs.get('logger')
    #img_path is must be a path to the .tif file of an AOP image product
    filename = os.path.split(img_path)[1]
    new_filename = '%s.hdr' % os.path.splitext(filename)[0]

    try:
        os.makedirs(output_port_path)
    except:
        pass

    # Copy input files to output
    for filename in glob('%s.*' % os.path.splitext(img_path)[0]):
        dest = os.path.join(output_port_path, os.path.split(filename)[1])
        copyfile(filename, dest)
        logit.debug('%s -> %s' % (filename, dest))

    #create empty hdr file
    hdr_file = open(os.path.join(output_port_path, new_filename), "w+")
    logit.debug('New hdr file: %s' % hdr_file)

    # Add fixed values hdr line
    hdr_file.write('ENVI\n')

    #open image in geoio
    try:
        img = geoio.DGImage(img_path)
    except Exception:
        # Not an ortho image
        img = geoio.GeoImage(img_path)

    #create ordered dictto have some contraol over writing order
    envi_dict = collections.OrderedDict()
    #add elements to the ODict
    envi_dict['description'] = '{Creating ENVI hdr file from AOP data}'
    envi_dict['sensor type'] = DG_SATID_TO_ENVI[img.meta.satid]
    envi_dict['lines'] = str(img.meta.shape[1])
    envi_dict['samples'] = str(img.meta.shape[2])
    envi_dict['bands'] = str(img.meta.shape[0])
    if envi_dict['bands'] == '3': # Condition for RGB images??
        band_indexes = [i for i, v in enumerate(img.meta.band_names) if v in RGB_BANDS]
        band_wavelengths = [img.meta.band_centers[index] for index in band_indexes]
        envi_dict['band_names'] = '{%s}' % ', '.join(RGB_BANDS)
        envi_dict['wavelength'] = '{%s}' % ', '.join(str(e) for e in band_wavelengths)
    else:
        envi_dict['band names'] = '{%s}' % ', '.join(str(e) for e in img.meta.band_names)
        envi_dict['wavelength'] = '{%s}' % ', '.join(str(e) for e in img.meta.band_centers)
    envi_dict['wavelength units'] = DG_WAVELENGTH_UNITS

    for entry, value in envi_dict.iteritems():
        #iterate through elements to write them out to file
        hdr_file.write('%s = %s\n' % (entry, value))

    #close file
    hdr_file.close()
