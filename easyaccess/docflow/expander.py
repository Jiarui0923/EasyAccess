from .document import Document

class Expander(Document):
    
    def __init__(self, content, title='', open=False):
        self.content = content
        self.title = title
        self.open = open
        
    @property    
    def markdown(self):
        if isinstance(self.content, Document): _content = self.content.html
        else: _content = str(self.content)
        if isinstance(self.title, Document): _title = self.title.html
        else: _title = str(self.title)
        if self.open: open_tag = ' open'
        else: open_tag = ''
        return f'<details {open_tag}>\n<summary>{_title}</summary>  \n{_content}  \n</details>  \n'
    