from pandas            import DataFrame
from matplotlib.figure import Figure
from types             import FunctionType

from .document import Document
from .plaintext import Text
from .sequence  import Sequence
from .table     import Table
from .image     import EmbeddedImage
from .code      import Code

class Magic(Document):
    
    _content_map = {
        str:          Text,
        list:         Sequence,
        dict:         Sequence,
        DataFrame:    Table,
        Figure:       EmbeddedImage,
        FunctionType: Code,
    }

    def __init__(self, content):
        for _type, _doc_class in self._content_map.items():
            if isinstance(content, _type):
                self._doc = _doc_class(content)
                break
    
    @property    
    def markdown(self): return self._doc.markdown
    @property
    def html(self): return self._doc.html