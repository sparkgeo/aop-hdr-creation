import glob2
import os
import sys
import logging

from envi_hdr import create_hdr
from gbdx_task_interface import GbdxTaskInterface


class AOPToEnviHdr(GbdxTaskInterface):

    def invoke(self):
        image_port_path = self.get_input_data_port('image')
        output_port_path = self.get_output_data_port('output_data')

        try:
            os.makedirs(output_port_path)
        except Exception as e:
            self.logger.exception(e)

        # Set-up logger
        logger = logging.getLogger('aoptoenvi')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        hdlr = logging.FileHandler(os.path.join(output_port_path, 'aop_envi_hdr.log'))
        hdlr.setLevel(logging.DEBUG)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        std_out = logging.StreamHandler(sys.stdout)
        std_out.setLevel(logging.DEBUG)
        std_out.setFormatter(formatter)
        logger.addHandler(std_out)

        logger.debug("Start Log: ")

        all_files_lower = glob2.glob('%s/**/*.tif' % image_port_path)
        all_files_upper = glob2.glob('%s/**/*.TIF' % image_port_path)
        all_files = all_files_lower + all_files_upper

        if len(all_files) == 0:
            raise ValueError("No image files found in image port.")

        logger.debug("%s Images found" % len(all_files))

        for img_file in all_files:
            logger.debug('Input Image: %s' % img_file)
            new_output_port_path = os.path.join(output_port_path, os.path.split(img_file)[0][len(image_port_path)+1:])
            logger.debug('Output_path: %s' % new_output_port_path)
            try:
                create_hdr(
                    img_file,
                    new_output_port_path,
                    logger=logger
                )
            except Exception as e:
                logger.exception(e)

        self.reason = 'Successfully created Header files'


if __name__ == "__main__":
    with AOPToEnviHdr() as task:
        task.invoke()
