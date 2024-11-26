from .document import Document

class Sequence(Document):
    
    def __init__(self, seq, num_index=False):
        self._seq = seq
        self._num_index = num_index
    
    @property     
    def markdown(self):
        if isinstance(self._seq, list):
            items = [f'{i(tab=True)}' if isinstance(i, Document) else f'{i}'
                     for i in self._seq]
        elif isinstance(self._seq, dict):
            items = [f'**{i}**: {v(tab=True)}' if isinstance(v, Document) else f'**{i}**: {v}'
                     for i, v in self._seq.items()]
        else:
            raise TypeError

        if self._num_index:
            return ''.join([f'{index} {i}  \n' for index, i in enumerate(items)])
        else:
            return ''.join([f'- {i}  \n' for i in items])