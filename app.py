from glob import glob
import os
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


        for img_file in glob('%s/*.tif' % image_port_path):
            create_hdr(
                os.path.join(image_port_path, img_file),
                output_port_path,
            )

        self.reason = 'Successfully created Header file'


if __name__ == "__main__":
    with AOPToEnviHdr() as task:
        task.invoke()
