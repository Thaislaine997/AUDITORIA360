"""
Redirect module to consolidate services in src.services
This module redirects all imports to the centralized services in src.services
to avoid duplication while maintaining backward compatibility.
"""

# Import everything from the centralized services that exist
from src.services.auth_service import *
from src.services.cache_service import *
from src.services.enhanced_notification_service import *
from src.services.openai_service import *
from src.services.payroll_service import *
from src.services.user_service import *

# Re-export communication gateway
from src.services.communication_gateway import *

# Re-export OCR service
from src.services.ocr import *

# Re-export storage service  
from src.services.storage import *