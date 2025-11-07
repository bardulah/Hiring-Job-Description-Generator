"""
Logging configuration for the hiring system.
"""

import logging
import os
from pathlib import Path
from typing import Optional
from .config import config


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    # Get config values
    if level is None:
        level = config.get('logging.level', 'INFO')

    if log_file is None:
        log_file = config.get('logging.log_file', 'logs/hiring_system.log')

    log_format = config.get(
        'logging.format',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Get logger for our package
    logger = logging.getLogger('hiring_system')
    logger.setLevel(getattr(logging, level.upper()))

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(f'hiring_system.{name}')


# Default logger instance
logger = setup_logging()
