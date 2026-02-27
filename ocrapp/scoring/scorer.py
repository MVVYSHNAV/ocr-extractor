import re
import math
from langdetect import detect_langs
import logging

logger = logging.getLogger(__name__)

class TextScorer:
    """
    Scoring mechanism to evaluate the quality of extracted text.
    Evaluates word-to-character density, garbage/symbol ratio, 
    language confidence, and checks for typical OCR noise.
    """
    
    @staticmethod
    def score(text: str) -> float:
        if not text or not text.strip():
            return 0.0
            
        text = text.strip()
        length = len(text)
        
        # 1. Base length score (logarithmic so large documents don't automatically win)
        base_score = min(math.log1p(length) * 10, 100.0)
        
        # 2. Garbage / Symbol ratio
        # Non-alphanumeric, non-whitespace, non-standard punctuation are often OCR noise
        garbage_pattern = re.compile(r'[^\w\s.,!?;:\'"()[\]{}-]')
        garbage_matches = garbage_pattern.findall(text)
        garbage_ratio = len(garbage_matches) / length if length > 0 else 1.0
        
        garbage_penalty = garbage_ratio * 150.0  # Heavy penalty for garbage
        
        # 3. Word density (avg word length)
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)
        
        avg_word_length = length / word_count if word_count > 0 else 0
        word_density_score = 0.0
        if 3 <= avg_word_length <= 12:
            word_density_score = 25.0  # Healthy word density, typical of real text
        elif avg_word_length > 25:
            word_density_score = -40.0 # Likely missed spaces, fused words (common OCR error)
        elif avg_word_length < 2:
            word_density_score = -40.0 # Fragmented single chars
            
        # 4. Language Confidence (using a sample to avoid performance hit on huge files)
        sample = text[:5000]
        lang_score = 0.0
        try:
            langs = detect_langs(sample)
            if langs:
                # Top probability acts as confidence
                lang_score = langs[0].prob * 40.0
        except Exception:
            # langdetect might fail if there's no recognizable text
            pass
            
        # 5. Typical OCR noise penalties
        ws_penalty = 0.0
        # Excessive consecutive newlines or lots of excessive spaces
        if re.search(r'\n{5,}', text) or re.search(r' {6,}', text):
            ws_penalty = 15.0
            
        # Single characters separated by spaces (e.g. "H e l l o")
        spaced_chars_pattern = re.compile(r'\b(?:\w\s){4,}\w\b')
        if spaced_chars_pattern.search(text):
            ws_penalty += 20.0
            
        # Final Score Calculation
        final_score = base_score - garbage_penalty + word_density_score + lang_score - ws_penalty
        
        # Log components for debugging
        logger.debug(f"Scoring breakdown | Base: {base_score:.1f}, "
                     f"Garbage penalty: -{garbage_penalty:.1f}, "
                     f"Word density: {word_density_score:.1f}, "
                     f"Lang score: {lang_score:.1f}, "
                     f"WS/Noise penalty: -{ws_penalty:.1f} -> Total: {final_score:.1f}")
                     
        return max(0.0, final_score)
