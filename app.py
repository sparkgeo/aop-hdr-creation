from glob import glob
import os
import sys
import logging

from aop_to_envi_hdr import create_hdr
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

        hdlr = logging.FileHandler(os.path.join(output_port_path, 'app.log'))
        hdlr.setLevel(logging.DEBUG)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        std_out = logging.StreamHandler(sys.stdout)
        std_out.setLevel(logging.DEBUG)
        std_out.setFormatter(formatter)
        logger.addHandler(std_out)

        logger.debug('Start: %s' % glob('%s/*.tif' % image_port_path))

        for img_file in glob('%s/*.tif' % image_port_path):
            logger.debug('Input Image: %s' % img_file)
            create_hdr(
                os.path.join(image_port_path, img_file),
                output_port_path,
                logger=logger
            )

        self.reason = 'Successfully created Header file'


if __name__ == "__main__":
    with AOPToEnviHdr() as task:
        task.invoke()
