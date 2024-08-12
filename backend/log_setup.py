import logging
import re

logger_singleton = None

class SimpleLogFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            # Truncate long strings in log messages
            def truncate_field(field_name, max_length=40):
                pattern = fr"('{field_name}': '([^'\\]*(?:\\.[^'\\]*)*)')"
                matches = re.finditer(pattern, record.msg)
                for match in matches:
                    full_field = match.group(1)
                    field_content = match.group(2)
                    truncated_field = f"'{field_name}': '{field_content[:max_length]}...'" if len(field_content) > max_length else full_field
                    record.msg = record.msg.replace(full_field, truncated_field)

            # Apply truncation for relevant fields
            truncate_field('text')
            truncate_field('content')
            truncate_field('transcription')
            truncate_field('response')

        return True

def logger_initialisation():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    # Add the custom filter to the handler
    ch.addFilter(SimpleLogFilter())

    logger.addHandler(ch)

    return logger

def get_logger():
    global logger_singleton
    if logger_singleton is None:
        logger_singleton = logger_initialisation()
    return logger_singleton