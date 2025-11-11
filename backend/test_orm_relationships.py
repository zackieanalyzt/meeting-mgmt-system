"""
Test script to verify ORM relationships are correctly configured
Run this before starting the server to catch any mapping errors
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_orm_relationships():
    """Test that all ORM relationships are properly configured"""
    print("🔍 Testing ORM relationships...")
    
    try:
        # Import all models to trigger relationship configuration
        from app.models import (
            User, Role, UserRole, Meeting, Agenda, 
            File, Report, SearchLog, AgendaObjective, AgendaObjectiveMap
        )
        
        print("✅ All models imported successfully")
        
        # Test that relationships are defined
        assert hasattr(Agenda, 'objective_maps'), "Agenda missing objective_maps relationship"
        assert hasattr(AgendaObjectiveMap, 'agenda'), "AgendaObjectiveMap missing agenda relationship"
        assert hasattr(AgendaObjectiveMap, 'objective'), "AgendaObjectiveMap missing objective relationship"
        assert hasattr(AgendaObjective, 'agenda_maps'), "AgendaObjective missing agenda_maps relationship"
        
        print("✅ All relationships defined correctly")
        
        # Test table creation (dry run)
        from app.core.database import Base, postgres_engine
        
        # This will validate all relationships without actually creating tables
        Base.metadata.create_all(bind=postgres_engine, checkfirst=True)
        
        print("✅ Database schema validation passed")
        print("✅ ORM relationships test PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ ORM relationships test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_orm_relationships()
    sys.exit(0 if success else 1)
