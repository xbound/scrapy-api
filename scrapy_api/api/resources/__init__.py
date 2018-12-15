from .ping import api as ping_namespace
from .document import api as document_namespace
from .image import api as image_namespace

__all__ = [
    'ping_namespace',
    'document_namespace',
    'image_namespace',
]