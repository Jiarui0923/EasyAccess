import matplotlib
import base64
import io
import os

import matplotlib.pyplot
from .document import Document

class EmbeddedImage(Document):
    
    def __init__(self, image):
        if isinstance(image, matplotlib.figure.Figure):
            img_stream = io.BytesIO()
            image.savefig(img_stream, format='jpg', bbox_inches='tight')
            img_stream.seek(0)
            img_base64 = base64.b64encode(img_stream.read()).decode()
            self._image_base64 = f'<img src="data:image/jpg;base64,{img_base64}">'
            image.clear()
            matplotlib.pyplot.close(image)
        elif os.path.isfile(image):
            with open(image, 'rb') as f:
                img_stream = io.BytesIO(f.read())
                img_stream.seek(0)
                img_base64 = base64.b64encode(img_stream.read()).decode()
                self._image_base64 = f'<img src="data:image/jpg;base64,{img_base64}">'
        else:
            raise TypeError
    
    @property     
    def markdown(self):
        return f'{self._image_base64}   \n\n'