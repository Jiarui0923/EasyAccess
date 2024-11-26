from .document import Document

class Title(Document):
    
    def __init__(self, context='', level=1):
        if level < 1 or level > 5:
            raise ValueError(f'Title level can be 1~5. {level} is not valid')
        self._level = level
        self._context = context
    
    @property   
    def markdown(self):
        return f'{"".join(["#" for _ in range(self._level)])} {self._context}  \n'
    
    
class Text(Document):
    
    def __init__(self, text):
        self._text = text
        
    @property   
    def markdown(self):
        return f'{self._text}  \n'