import abc
import logging

class BaseExtractor(abc.ABC):
    """
    Base class for all document extractors.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the extractor."""
        pass
        
    @abc.abstractmethod
    def extract(self, file_path: str) -> str:
        """
        Extracts text from the given file path.
        Returns the extracted text as a string.
        Should raise appropriate exceptions on failure.
        """
        pass
