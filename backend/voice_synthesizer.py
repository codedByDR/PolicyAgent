"""
Voice Synthesis Module
Converts policy explanations to voice notes in multiple languages
Uses pyttsx3 as primary offline TTS engine (more reliable than gTTS)
"""

import pyttsx3
import os
import threading
from pathlib import Path
from datetime import datetime
import uuid


class VoiceSynthesizer:
    """Generate voice notes from text using offline text-to-speech"""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'ja': 'Japanese',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'zh-cn': 'Chinese Simplified',
        'bn': 'Bengali',
        'te': 'Telugu',
        'ta': 'Tamil',
        'ml': 'Malayalam',
    }
    
    # Store async tasks
    _pending_tasks = {}
    _completed_tasks = {}
    
    def __init__(self, output_dir: str = "voice_outputs"):
        """Initialize voice synthesizer with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize pyttsx3 engine
        try:
            self.engine = pyttsx3.init()
            print("[Voice Synthesizer] pyttsx3 engine initialized successfully")
        except Exception as e:
            print(f"[Voice Synthesizer] Error initializing pyttsx3: {str(e)}")
            self.engine = None
    
    def synthesize_voice_async(self, text: str, language: str = 'en', 
                                slow: bool = False) -> dict:
        """
        Start voice synthesis in background and return immediately
        
        Args:
            text: Text to convert to speech
            language: Language code (default: 'en')
            slow: Slow speech (default: False)
            
        Returns:
            Dictionary with task_id for polling status
        """
        # Create task ID
        task_id = str(uuid.uuid4())[:8]
        
        # Store pending task
        self._pending_tasks[task_id] = {
            "status": "processing",
            "language": language
        }
        
        # Start background thread
        thread = threading.Thread(
            target=self._synthesize_in_background,
            args=(task_id, text, language, slow)
        )
        thread.daemon = True
        thread.start()
        
        return {
            "success": True,
            "task_id": task_id,
            "status": "processing",
            "message": "Voice synthesis started in background"
        }
    
    def _synthesize_in_background(self, task_id: str, text: str, language: str, slow: bool):
        """Internal method to synthesize voice in background thread"""
        try:
            if not self.engine:
                self._completed_tasks[task_id] = {
                    "success": False,
                    "message": "Text-to-speech engine not initialized"
                }
                return
            
            # Limit text length
            if len(text) > 3000:
                text = text[:3000] + "..."
            
            # Create unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"policy_explanation_{timestamp}_{task_id}.wav"
            file_path = self.output_dir / filename
            
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"[Voice Synthesizer] Background: Creating {filename}")
            
            # Configure and generate speech
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate * 0.85 if slow else rate)
            
            available_voices = self.engine.getProperty('voices')
            if available_voices:
                self.engine.setProperty('voice', available_voices[0].id)
            
            self.engine.save_to_file(text, str(file_path))
            self.engine.runAndWait()
            
            # Store result
            if file_path.exists():
                self._completed_tasks[task_id] = {
                    "success": True,
                    "message": "Voice note created successfully",
                    "file_path": str(file_path),
                    "filename": filename,
                    "language": self.SUPPORTED_LANGUAGES.get(language, language)
                }
            else:
                self._completed_tasks[task_id] = {
                    "success": False,
                    "message": "Voice file was not created"
                }
                
        except Exception as e:
            print(f"[Voice Synthesizer] Background error: {str(e)}")
            self._completed_tasks[task_id] = {
                "success": False,
                "message": f"Error: {str(e)}"
            }
        finally:
            # Remove from pending
            if task_id in self._pending_tasks:
                del self._pending_tasks[task_id]
    
    def get_task_status(self, task_id: str) -> dict:
        """Get status of async voice synthesis task"""
        if task_id in self._completed_tasks:
            result = self._completed_tasks[task_id]
            # Clean up completed task after returning
            del self._completed_tasks[task_id]
            return result
        
        if task_id in self._pending_tasks:
            return {
                "success": True,
                "status": "processing",
                "message": "Voice synthesis in progress..."
            }
        
        return {
            "success": False,
            "message": "Task not found"
        }
    
    # Keep sync version for backward compatibility
    def synthesize_voice(self, text: str, language: str = 'en', 
                        slow: bool = False) -> dict:
        """Synchronous voice synthesis - returns immediately with task_id for polling"""
        return self.synthesize_voice_async(text, language, slow)
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        return {
            "languages": self.SUPPORTED_LANGUAGES,
            "count": len(self.SUPPORTED_LANGUAGES)
        }
    
    @staticmethod
    def chunk_text_for_tts(text: str, max_length: int = 3000) -> list:
        """
        Split text into chunks suitable for TTS
        
        Args:
            text: Text to split
            max_length: Maximum length of each chunk
            
        Returns:
            List of text chunks
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
