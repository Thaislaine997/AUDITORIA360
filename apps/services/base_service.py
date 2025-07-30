"""
Base service class for AUDITORIA360 application services.
Implements common patterns for multi-tenant isolation and business logic encapsulation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import and_

from apps.models.auth_models import User

T = TypeVar('T')

class BaseService(ABC, Generic[T]):
    """
    Base service class that provides common functionality for all business services.
    Ensures multi-tenant isolation and standardizes service patterns.
    """
    
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
        self.tenant_id = self._get_tenant_id(current_user)
    
    def _get_tenant_id(self, user: User) -> str:
        """Extract tenant ID from user context"""
        # This could be based on user.company_id, user.organization_id, etc.
        # For now, using a simple approach
        return getattr(user, 'company_id', 'default')
    
    def _apply_tenant_filter(self, query, model_class=None):
        """
        Apply tenant isolation filter to any query automatically.
        This ensures data isolation across tenants.
        """
        if model_class and hasattr(model_class, 'tenant_id'):
            return query.filter(model_class.tenant_id == self.tenant_id)
        return query
    
    def _ensure_tenant_access(self, entity) -> bool:
        """
        Verify that the current user has access to the given entity.
        Raises exception if access is denied.
        """
        if hasattr(entity, 'tenant_id') and entity.tenant_id != self.tenant_id:
            raise PermissionError(f"Access denied to resource from tenant {entity.tenant_id}")
        return True
    
    @abstractmethod
    def get_model_class(self) -> type:
        """Return the main model class this service operates on"""
        pass
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new entity with automatic tenant assignment"""
        # Add tenant_id to data if the model supports it
        model_class = self.get_model_class()
        if hasattr(model_class, 'tenant_id'):
            data['tenant_id'] = self.tenant_id
        
        entity = model_class(**data)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID with tenant isolation"""
        model_class = self.get_model_class()
        query = self.db.query(model_class).filter(model_class.id == entity_id)
        query = self._apply_tenant_filter(query, model_class)
        entity = query.first()
        
        if entity:
            self._ensure_tenant_access(entity)
        
        return entity
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with tenant isolation and pagination"""
        model_class = self.get_model_class()
        query = self.db.query(model_class)
        query = self._apply_tenant_filter(query, model_class)
        
        return query.offset(skip).limit(limit).all()
    
    def update(self, entity_id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update entity with tenant access validation"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        
        self._ensure_tenant_access(entity)
        
        # Update fields
        for field, value in data.items():
            if hasattr(entity, field) and field != 'tenant_id':  # Prevent tenant_id changes
                setattr(entity, field, value)
        
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity with tenant access validation"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        
        self._ensure_tenant_access(entity)
        
        self.db.delete(entity)
        self.db.commit()
        return True
    
    def count(self) -> int:
        """Count entities with tenant isolation"""
        model_class = self.get_model_class()
        query = self.db.query(model_class)
        query = self._apply_tenant_filter(query, model_class)
        return query.count()


class ServiceFactory:
    """
    Factory for creating service instances with proper dependency injection.
    Ensures all services are properly configured with database and user context.
    """
    
    @staticmethod
    def create_service(service_class: type, db: Session, current_user: User):
        """Create a service instance with proper context"""
        return service_class(db=db, current_user=current_user)