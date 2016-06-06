import geoio, os, collections

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

def create_hdr(aop_path, debug="no", description = None):
    #aop_path is assumed to be a path to the .tif file of an AOP image product

    #create empty hdr file
    hdr_file = open(os.path.splitext(aop_path)[0] + ".hdr", "w+")
    # Allow for manual description
    if description == None:
        description = 'Creating ENVI hdr file from AOP data [' + date.today().isoformat() + ']'

    # Add fixed values hdr line
    hdr_file.write('ENVI\n')

    #open image in geoio
    img = geoio.DGImage(aop_path)

    if debug == 'yes':
        print "*****************************"
        print img.print_img_summary

    #create ordered dictto have some contraol over writing order
    envi_dict = collections.OrderedDict()
    #add elements to the ODict
    envi_dict['description'] = '{' + description + '}'
    envi_dict['sensor type'] = DG_SATID_TO_ENVI[img.meta.satid]
    envi_dict['lines'] = str(img.meta.shape[1])
    envi_dict['samples'] = str(img.meta.shape[2])
    envi_dict['bands'] = str(img.meta.shape[0])
    envi_dict['band names'] = '{\n' + "  " + ", ".join(str(e) for e in img.meta.band_names) + '}'
    envi_dict['wavelength'] = '{\n' + "  " + ", ".join(str(e) for e in img.meta.band_centers) + '}'
    envi_dict['wavelength units'] = DG_WAVELENGTH_UNITS

    for entry, value in envi_dict.iteritems():
        #iterate through elements to write them out to file
        hdr_file.write(entry + " = " + value + '\n')

    #close file
    hdr_file.close()