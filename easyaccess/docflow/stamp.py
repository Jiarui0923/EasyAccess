from datetime import datetime
from uuid import uuid4
from .document import Document

class DateTimeStamp(Document):
    
    def __init__(self, timefmt='%d-%m-%Y %H:%M:%S %Z', text=None):
        self._timefmt = timefmt
        self._text = text
    
    @property   
    def markdown(self):
        _time = datetime.now().astimezone().strftime(self._timefmt)
        if self._text is None: return f'`{_time}`  \n'
        else: return f'`{_time} {self._text}`  \n'
        
        
class UUIDStamp(Document):
    
    def __init__(self, text=None):
        self._text = text
    
    @property   
    def markdown(self):
        _uuid = str(uuid4()).upper()
        if self._text is None: return f'`{_uuid}`  \n'
        else: return f'`{_uuid} {self._text}`  \n'