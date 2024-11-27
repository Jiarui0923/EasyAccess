import websocket
import json


class WebSocket(object):
    
    def __init__(self, host, header):
        self._client = websocket.WebSocket()
        self._client.connect(url=host, header=header)
        
    def close(self): self._client.close()
    def send(self, text): self._client.send(text)
    def recv(self): return self._client.recv()
    def query(self, text):
        self.send(text=text)
        return self.recv()
    @property
    def connected(self): return self._client.connected
    

class EasyAccessWebSocket(WebSocket):
    def query(self, text):
        self.send(text=text)
        data = json.loads(self.recv())
        if 'success' in data: self.close()
        return data
            