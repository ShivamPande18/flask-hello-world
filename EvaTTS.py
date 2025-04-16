import asyncio
import edge_tts

class EdgeTTSSpeaker:
    """A class that handles text-to-speech conversion using edge-tts."""
    
    VOICES = [
        'en-AU-NatashaNeural', 
        'en-AU-WilliamNeural', 
        'en-CA-ClaraNeural', 
        'en-CA-LiamNeural', 
        'en-GB-LibbyNeural', 
        'en-GB-MaisieNeural'
    ]
    
    def __init__(self, default_voice_index=4):
        """Initialize with a default voice."""
        self.default_voice = self.VOICES[default_voice_index]
    
    async def _tts_async(self, text, voice=None):
        """Internal async function to perform the TTS operation."""
        selected_voice = voice if voice else self.default_voice
        
        output_file = "test.mp3"
            
        communicate = edge_tts.Communicate(text, selected_voice)
        await communicate.save(output_file)
        return output_file
    
    def tts(self, text, voice=None):
        """
        Convert text to speech and save as an audio file.
        
        Args:
            text (str): The text to convert to speech
            voice (str, optional): The voice to use. Defaults to the initialized default voice.
            output_file (str, optional): The output file path. Defaults to "speech_output.mp3".
            
        Returns:
            str: The path to the created audio file
        """
        # Create a new event loop for this function call
        loop = asyncio.new_event_loop()
        try:
            # Set the event loop and run the async function
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._tts_async(text, voice))
        finally:
            # Clean up
            loop.close()
    

    def list_voices(self):
        """Return the list of available voices."""
        return self.VOICES
