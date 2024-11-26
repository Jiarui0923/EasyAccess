import markdown
import os

_style_sheet_path = os.path.join(os.path.dirname(__file__), 'property/github-markdown.css')
_style_header = '''
<style>
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
        box-shadow: 10px 5px 5px grey;
        border: solid black 0.2px;
	}

	@media (max-width: 767px) {
		.markdown-body {
			padding: 15px;
		}
	}
</style>
'''

class Document:
    
    def __init__(self, *args):
        self._documents = list(args)
        
    def _tab_append(self, obj):
        lines = obj.split('\n')
        return f'{lines[0]}\n' + ''.join([f'\t{i}\n' for i in lines[1:]])
    
    @property    
    def markdown(self): return ''.join([d.markdown for d in self._documents])
    @property
    def html(self): return markdown.markdown(self.markdown, extensions=['tables'])
    
    def __repr__(self): return self.markdown
    def __call__(self, tab=False):
        if tab: return self._tab_append(self.markdown, extensions=['tables'])
        else: return self.markdown
    def _repr_markdown_(self):
        return self.markdown
    
    def add(self, doc):
        if isinstance(doc, Document): self._documents.append(doc)  
        else: raise TypeError('Require Document Type Node')    
    def save(self, path, format='markdown'):
        if format == 'markdown':
            with open(path, 'w') as f: f.write(self.markdown)
        elif format == 'html':
            with open(_style_sheet_path, 'r') as f: style_sheet = f.read()
            with open(path, 'w') as f: f.write(f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<article class="markdown-body">\n{self.html}\n</article>\n<style>\n{style_sheet}\n</style>\n{_style_header}')
        else: raise ValueError(f'Format {format} Not Support')