"""
Tassi Python SDK
================

Un SDK Python pour interagir avec l'API Tassi.
"""

from .tassi import Tassi
from .tassi_object import TassiObject
from .resource import Resource
from .requestor import Requestor
from .package import Package
from .shipment import Shipment
from .marketplace import Marketplace
from .error import (
    TassiError,
    InvalidRequestError,
    ApiConnectionError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)
from .util import array_to_tassi_object

__version__ = "1.0.0"
__author__ = "Tassi Team"
__email__ = "dev@tassi.com"

__all__ = [
    "Tassi",
    "TassiObject",
    "Resource",
    "Requestor",
    "Package",
    "Shipment",
    "Marketplace",
    "TassiError",
    "InvalidRequestError",
    "ApiConnectionError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "array_to_tassi_object"
]