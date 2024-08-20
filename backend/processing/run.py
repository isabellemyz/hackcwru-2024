from processing.conversation import Conversation
from processing.transcribe import Transcription
import asyncio
from starlette.websockets import WebSocketDisconnect

conversation = Conversation()

class Combined: 
    def __init__(self, websocket, conversation, transcription):
        self.websocket = websocket
        self.conversation = conversation
        self.transcription = Transcription(websocket, conversation)
    
    async def transcribe_audio(self):
        await self.transcription.transcribe_audio()

    async def manage_conversation(self, client):
        await self.transcription.manage_transcription(client)

    async def run(self, client):
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self.transcribe_audio())
                tg.create_task(self.manage_conversation(client))
        except* WebSocketDisconnect:
            print('Client disconnected')
        finally:
            await self.transcription.websocket.close()