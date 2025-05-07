import traceback
import logging


class SyncError(Exception):
    def __init__(self, message, context=None, original_exception=None):
        self.context = context
        self.original_exception = original_exception
        super().__init__(message)

class APIError(SyncError): pass
class ModelError(SyncError): pass
class ParsingError(SyncError): pass
class DatabaseError(SyncError): pass
class TableNotFoundError(DatabaseError): pass
class MetadataNotFoundError(DatabaseError): pass
class CompositeKeyError(DatabaseError): pass



def log_error(logger: logging.Logger, e: SyncError):
    logger.error(f"{type(e).__name__}: {e}")
    if hasattr(e, 'context') and e.context:
        logger.error(f"Context: {e.context}")
    if hasattr(e, 'original_exception') and e.original_exception:
        logger.error("Original traceback:\n" + ''.join(traceback.format_exception(
            None, e.original_exception, e.original_exception.__traceback__)))
