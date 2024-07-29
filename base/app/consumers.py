import json
from channels.generic.websocket import WebsocketConsumer

class DownloadProgressConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message back to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_progress(self, progress):
        self.send(text_data=json.dumps({
            'progress': progress
        }))
