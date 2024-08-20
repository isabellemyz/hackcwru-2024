import asyncio
from deepgram import (
    DeepgramClient, DeepgramClientOptions, LiveTranscriptionEvents, LiveOptions
)
from processing.conversation import Conversation
from log_setup import get_logger
import os
from dotenv import load_dotenv

load_dotenv()

logger = get_logger()

DEEPGRAM_TTS_URL = 'https://api.deepgram.com/v1/speak?model=aura-luna-en'
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

conversation = Conversation()

deepgram_config = DeepgramClientOptions(options={'keepalive': 'true'})
deepgram = DeepgramClient(DEEPGRAM_API_KEY, config=deepgram_config)
dg_connection_options = LiveOptions(
    model='nova-2',
    language='en',
    smart_format=True,
    interim_results=True,
    utterance_end_ms='1000',
    vad_events=True,
    endpointing=500,
)

class Transcription:
    def __init__(self, websocket, conversation):
        self.websocket = websocket
        self.transcript_parts = []
        self.transcript_queue = asyncio.Queue()
        self.conversation = conversation  
        self.finish_event = asyncio.Event()
    
    async def transcribe_audio(self):
        async def on_message(self_handler, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                self.transcript_parts.append(sentence)
                await self.transcript_queue.put({'type': 'transcript_final', 'content': sentence})
                if result.speech_final:
                    full_transcript = ' '.join(self.transcript_parts)
                    self.transcript_parts = []
                    await self.transcript_queue.put({'type': 'speech_final', 'content': full_transcript})
            else:
                await self.transcript_queue.put({'type': 'transcript_interim', 'content': sentence})
        
        async def on_utterance_end(self_handler, utterance_end, **kwargs):
            if len(self.transcript_parts) > 0:
                full_transcript = ' '.join(self.transcript_parts)
                self.transcript_parts = []
                await self.transcript_queue.put({'type': 'speech_final', 'content': full_transcript})

        dg_connection = deepgram.listen.asynclive.v('1')
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        if await dg_connection.start(dg_connection_options) is False:
            raise Exception('Failed to connect to Deepgram')
        
        try:
            while not self.finish_event.is_set():
                # Receive audio stream from the client and send it to Deepgram to transcribe it
                data = await self.websocket.receive_bytes()
                await dg_connection.send(data)
        finally:
            await dg_connection.finish()
        
    async def manage_transcription(self, client):
        while not self.finish_event.is_set():
            transcript = await self.transcript_queue.get()
            if transcript['type'] == 'speech_final':
                user_input = transcript['content']
                self.conversation.add_message("user", user_input)

                
                # Call get_response with the user input
                assistant_response = self.conversation.get_response(user_input, client)
                self.conversation.add_message("assistant", assistant_response)
                
                # Send the assistant's response back to the client
                await self.websocket.send_json({'type': 'assistant', 'content': assistant_response})

                
                
                # Optionally generate audio if needed
                # audio_data = get_response_audio(assistant_response, client)
                # await self.websocket.send_bytes(audio_data)

                if self.conversation.get_total_tokens() >= self.conversation.token_threshold:
                    self.conversation.summarize_conversation(client)
            else:
                await self.websocket.send_json(transcript)

    



