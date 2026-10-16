import json
import logging
import threading
import time
import queue
from typing import Dict, Any, Optional
import torch
from whisper_live import st_models
import threading
from transformers import M2M100ForConditionalGeneration
from whisper_live.backend.tokenization_small100 import SMALL100Tokenizer

from whisper_live.backend.base import ServeClientBase


class ServeClientTranslation(ServeClientBase):
    """
    Handles translation of completed transcription segments in a separate thread.
    Reads from a queue populated by the transcription backend and sends translated
    segments back to the client via WebSocket.
    """
    
    # PARCHE LOCAL: el modelo de traduccion era UNO POR CLIENTE. Cada Start cargaba
    # otra copia de SMALL100 (639 MiB en fp16) y las viejas solo se soltaban si el
    # cliente se desconectaba limpiamente, cosa que no pasa cuando cierras la
    # pestana de golpe o el servidor peta. A los 2-3 intentos: CUDA out of memory.
    # El modelo es el mismo para todos (el idioma destino lo pone el TOKENIZER, que
    # es diminuto y sigue siendo por cliente), asi que se comparte una sola copia.
    MODELO_COMPARTIDO = None
    MODELO_COMPARTIDO_DEVICE = None
    MODELO_COMPARTIDO_LOCK = threading.Lock()

    def __init__(
        self,
        client_uid,
        websocket,
        translation_queue,
        target_language="fr", 
        send_last_n_segments=10,
        model_name="alirezamsh/small100"
    ):
        """
        Initialize the translation client.
        
        Args:
            client_uid (str): Unique identifier for the client
            websocket: WebSocket connection to the client
            translation_queue (queue.Queue): Queue containing completed segments to translate
            target_language (str): Target language code (default: "fr" for French)
            send_last_n_segments (int): Number of recent translated segments to send
            model_name (str): Translation model name to use
        """
        super().__init__(client_uid, websocket, send_last_n_segments)
        self.translation_queue = translation_queue
        self.target_language = target_language
        self.model_name = model_name
        self.translated_segments = []
        self.segmento_en_curso = None   # PARCHE LOCAL: la linea provisional en vivo
        self.translation_model = None
        self.tokenizer = None
        self.device = None
        self.model_loaded = False
        self.load_translation_model()
        
    def load_translation_model(self):
        """Load the translation model and tokenizer."""
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # Stream Transcription: the client may send the translator to the CPU
            if st_models.translator_on_cpu():
                self.device = torch.device("cpu")
            logging.info(f"Loading translation model on device: {self.device}")
            
            # PARCHE LOCAL: cargar en float16 en la GPU.
            # from_pretrained() sin torch_dtype carga en float32: SMALL100 son ~330M
            # parametros, o sea ~1,3 GB de VRAM para un modelo que en fp16 ocupa la mitad.
            # En una grafica de 6 GB compartida con Whisper y con otros procesos, ese giga de
            # mas es la diferencia entre que quepa 'medium' o no.
            # En CPU se queda en float32: fp16 en CPU va lentisimo y encima no ahorra nada.
            with ServeClientTranslation.MODELO_COMPARTIDO_LOCK:
                # shared copy on the other device: drop it and load it here
                if (ServeClientTranslation.MODELO_COMPARTIDO is not None and
                        ServeClientTranslation.MODELO_COMPARTIDO_DEVICE != self.device.type):
                    ServeClientTranslation.MODELO_COMPARTIDO = None
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                if ServeClientTranslation.MODELO_COMPARTIDO is None:
                    if self.device.type == "cuda":
                        ServeClientTranslation.MODELO_COMPARTIDO = (
                            M2M100ForConditionalGeneration.from_pretrained(
                                self.model_name, torch_dtype=torch.float16
                            ).to(self.device))
                    else:
                        ServeClientTranslation.MODELO_COMPARTIDO = (
                            M2M100ForConditionalGeneration.from_pretrained(
                                self.model_name
                            ).to(self.device))
                    ServeClientTranslation.MODELO_COMPARTIDO_DEVICE = self.device.type
                    logging.info("Modelo de traduccion cargado (compartido)")
                else:
                    logging.info("Reutilizando el modelo de traduccion ya cargado")
                self.translation_model = ServeClientTranslation.MODELO_COMPARTIDO
            self.tokenizer = SMALL100Tokenizer.from_pretrained(self.model_name)
            self.tokenizer.tgt_lang = self.target_language
            
            self.model_loaded = True
            logging.info(f"Translation model loaded successfully. Target language: {self.target_language}")
        except Exception as e:
            logging.error(f"Failed to load translation model: {e}")
            self.translation_model = None
            self.tokenizer = None
            self.model_loaded = False
    
    def translate_text(self, text: str) -> str:
        """
        Translate a single text segment.
        
        Args:
            text (str): Text to translate
            
        Returns:
            str: Translated text or original text if translation fails
        """
        if not self.model_loaded or not text.strip():
            return text
            
        try:
            # Encode input and move to device
            encoded_input = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # REVERTIDO 2026-09-15 a peticion del usuario: se habia puesto
            # decodificacion greedy (num_beams=1 + max_new_tokens=128) el 25-ago para
            # bajar el retraso, pero la calidad de la traduccion se volvio mala de ver.
            # Vuelve a los defaults de SMALL100 (num_beams=5, max_length=256) = beam
            # search. Cuesta latencia; es una decision informada del usuario.
            # 🛑 NO volver a poner greedy por iniciativa propia.
            with torch.no_grad():
                generated_tokens = self.translation_model.generate(**encoded_input)
            
            # Decode output
            output = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            return output[0] if output else text
            
        except Exception as e:
            logging.error(f"Translation failed for text '{text}': {e}")
            return text
    
    def process_translation_queue(self):
        """
        Process segments from the translation queue.
        Continuously reads from the queue until None is received (exit signal).
        """
        logging.info(f"Starting translation processing for client {self.client_uid}")
        
        while not self.exit:
            try:
                # Get segment from queue with timeout
                segment = self.translation_queue.get(timeout=1.0)
                
                # Check for exit signal
                if segment is None:
                    logging.info(f"Received exit signal for translation client {self.client_uid}")
                    break
                    
                # PARCHE LOCAL: antes se descartaban los segmentos sin cerrar, asi que el
                # espanol no aparecia hasta que el segmento cerraba. Ahora el segmento en
                # curso tambien se traduce y viaja como ultima linea PROVISIONAL: se pinta
                # en vivo y se sustituye sola cuando llega la version definitiva.
                completado = segment.get("completed", False)

                original_text = segment.get("text", "")
                translated_text = self.translate_text(original_text)

                translated_segment = {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": translated_text,
                    "completed": completado,
                    "target_language": self.target_language
                }

                if completado:
                    self.translated_segments.append(translated_segment)
                    self.segmento_en_curso = None
                else:
                    # No se acumula: es provisional y se reemplaza en cada vuelta.
                    self.segmento_en_curso = translated_segment
                    # TRAZA TEMPORAL (quitar cuando se confirme): cada cuanto sale una
                    # linea provisional traducida y con que texto.
                    self._n_prov = getattr(self, "_n_prov", 0) + 1
                    logging.info("PROVISIONAL #%d: %r", self._n_prov, translated_text[:60])
                segments_to_send = self.prepare_translated_segments()
                self.send_translation_to_client(segments_to_send)
                
                self.translation_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error processing translation queue: {e}")
                continue
        
        logging.info(f"Translation processing ended for client {self.client_uid}")
    
    def prepare_translated_segments(self):
        """
        Prepare the last n translated segments to send to client.
        
        Returns:
            list: List of recent translated segments
        """
        if len(self.translated_segments) >= self.send_last_n_segments:
            cerrados = self.translated_segments[-self.send_last_n_segments:]
        else:
            cerrados = self.translated_segments[:]
        # PARCHE LOCAL: el segmento en curso va SIEMPRE el ultimo, para que el cliente
        # pinte la linea viva debajo de las ya cerradas.
        en_curso = getattr(self, "segmento_en_curso", None)
        if en_curso is not None:
            return cerrados + [en_curso]
        return cerrados
    
    def send_translation_to_client(self, translated_segments):
        """
        Send translated segments to the client via WebSocket.
        
        Args:
            translated_segments (list): List of translated segments to send
        """
        try:
            self.websocket.send(
                json.dumps({
                    "uid": self.client_uid,
                    "translated_segments": translated_segments,
                })
            )
        except Exception as e:
            logging.error(f"[ERROR]: Sending translation data to client: {e}")
    
    def speech_to_text(self):
        """
        Override parent method to handle translation processing.
        This method will be called when the translation thread starts.
        """
        self.process_translation_queue()
    
    def set_target_language(self, language: str):
        """
        Change the target language for translation.
        
        Args:
            language (str): New target language code
        """
        self.target_language = language
        if self.tokenizer:
            self.tokenizer.tgt_lang = language
            logging.info(f"Target language changed to: {language}")
    
    def cleanup(self):
        """Clean up translation resources."""
        logging.info(f"Cleaning up translation resources for client {self.client_uid}")
        self.exit = True
        
        try:
            self.translation_queue.put(None, timeout=1.0)
        except:
            pass
        
        self.translated_segments.clear()
        
        # OJO: no se borra el modelo, que es COMPARTIDO. Solo se suelta la referencia.
        # Borrarlo aqui se lo quitaria a cualquier otra captura viva.
        if self.translation_model:
            self.translation_model = None
        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
        
        if self.device and self.device.type == 'cuda':
            torch.cuda.empty_cache()
