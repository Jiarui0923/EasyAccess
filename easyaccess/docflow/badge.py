from .document import Document

class Badge(Document):
    
    def __init__(self, head='', tail='', color='2ea44f'):
        self._badge = f'![{head}-{tail}](https://img.shields.io/badge/{head}-{tail}-{color})'
    
    @property  
    def markdown(self):
        return f'{self._badge}  \n\n'

class IdenticalBadge(Document):
    
    def __init__(self):
        self._badge = '![DocFlow-AutoDoc](https://img.shields.io/badge/DocFlow-AutoDoc-2ea44f)'
    
    @property  
    def markdown(self):
        return f'{self._badge}  \n\n'