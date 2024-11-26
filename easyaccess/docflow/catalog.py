import markdown
from .document import Document
from .plaintext import Title

class Catalog(Document):

    def __init__(self, doc):
        if not isinstance(doc, Document) and '_documents' in doc.__dict__:
            raise TypeError(f'Catalog can only be used to create catalog for Document class, but received {type(doc)}.')
        self._titles = self._enumerate_title(doc)
        self._catalog = self._build_catalog(self._titles)
    
    def _build_catalog(self, titles):
        _catalog_text = lambda s_ : f'[{s_}](#{str(s_).lower().replace(" ", "-")})'
        _catalog_str = ''
        for (_level, _title) in titles:
            _catalog_head = '  '*_level + '- '
            _catalog_str += f'{_catalog_head}{_catalog_text(_title)}\n'
        return _catalog_str

    def _enumerate_title(self, _sub_doc):

        _title_stack = []
        for _module in _sub_doc._documents:
            if isinstance(_module, Title):
                _title_stack.append((_module._level, _module._context))
            if isinstance(_module, Document) and '_documents' in _module.__dict__:
                _sub_title_stack = self._enumerate_title(_module)
                _title_stack = _title_stack + _sub_title_stack
        return _title_stack
    
    @property    
    def markdown(self): return self._catalog
    @property
    def html(self): return markdown.markdown(self.markdown)