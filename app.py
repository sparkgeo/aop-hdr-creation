from glob import glob
import os
from aop_to_envi_hdr import create_hdr
from gbdx_task_interface import GbdxTaskInterface


class AOPToEnviHdr(GbdxTaskInterface):

    def invoke(self):
        image_port_path = self.get_input_data_port('image')

        file_names = glob('*.tif')

        if len(file_names) != 1:
            raise ValueError('ONLY ONE IMAGE FILE SUPPORTED. EITHER NONE OR MANY FILES WERE FOUND.')

        new_filename = os.path.join(image_port_path, file_names[0])

        create_hdr(new_filename)

        self.reason = 'Successfully created Header file'


if __name__ == "__main__":
    with AOPToEnviHdr() as task:
        task.invoke()
