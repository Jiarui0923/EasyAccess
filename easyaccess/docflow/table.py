import pandas as pd
from .document import Document

class Table(Document):
    
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError
        self._df = df
    
    @property    
    def markdown(self):
        return f'{self._df.to_markdown()}  \n\n'