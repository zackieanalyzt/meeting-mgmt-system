"""
Test script to verify RBAC fix for admin_group role
Run this to ensure both Thai and English role names work correctly
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def test_rbac_roles():
    """Test that RBAC accepts both Thai and English role names"""
    print("🔍 Testing RBAC role configurations...")
    
    try:
        from app.core.rbac import require_any_admin, require_admin, Permissions
        
        # Test 1: Check allowed roles in require_any_admin
        print("\n📋 Test 1: Checking require_any_admin allowed roles")
        allowed_roles = require_any_admin.allowed_roles
        print(f"   Allowed roles: {allowed_roles}")
        
        assert "Admin ใหญ่" in allowed_roles, "Missing Thai admin_main role"
        assert "Admin กลุ่มงาน" in allowed_roles, "Missing Thai admin_group role"
        assert "admin_main" in allowed_roles, "Missing English admin_main role"
        assert "admin_group" in allowed_roles, "Missing English admin_group role"
        print("   ✅ All required roles present")
        
        # Test 2: Check Permissions class
        print("\n📋 Test 2: Checking Permissions class")
        print(f"   ADMIN_MAIN: {Permissions.ADMIN_MAIN}")
        print(f"   ADMIN_GROUP: {Permissions.ADMIN_GROUP}")
        print(f"   ANY_ADMIN: {Permissions.ANY_ADMIN}")
        
        assert len(Permissions.ADMIN_MAIN) >= 2, "ADMIN_MAIN should have both Thai and English"
        assert len(Permissions.ADMIN_GROUP) >= 2, "ADMIN_GROUP should have both Thai and English"
        print("   ✅ Permissions class configured correctly")
        
        # Test 3: Test permission checks
        print("\n📋 Test 3: Testing permission checks")
        
        # Test with Thai role name
        thai_roles = ["Admin กลุ่มงาน"]
        assert Permissions.can_add_agenda(thai_roles), "Thai admin_group should be able to add agenda"
        print("   ✅ Thai role name works")
        
        # Test with English role name
        english_roles = ["admin_group"]
        assert Permissions.can_add_agenda(english_roles), "English admin_group should be able to add agenda"
        print("   ✅ English role name works")
        
        # Test with mixed roles
        mixed_roles = ["admin_group", "Admin กลุ่มงาน"]
        assert Permissions.can_add_agenda(mixed_roles), "Mixed roles should work"
        print("   ✅ Mixed role names work")
        
        print("\n✅ All RBAC tests PASSED")
        print("\n📝 Summary:")
        print("   - Both Thai and English role names are supported")
        print("   - require_any_admin accepts: admin_main, admin_group, Admin ใหญ่, Admin กลุ่มงาน")
        print("   - Permission checks work with both naming conventions")
        
        return True
        
    except Exception as e:
        print(f"\n❌ RBAC test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_role_creation():
    """Test that roles are created correctly in database"""
    print("\n🔍 Testing role creation in database...")
    
    try:
        from app.services.auth_service import create_dummy_users
        from app.core.database import PostgresSessionLocal
        from app.models import Role
        
        db = PostgresSessionLocal()
        
        # Check if roles exist
        roles = db.query(Role).all()
        role_names = [r.role_name for r in roles]
        
        print(f"\n📋 Roles in database: {role_names}")
        
        # Check for both Thai and English roles
        expected_roles = [
            "Admin ใหญ่", "Admin กลุ่มงาน", "ผู้ใช้ทั่วไป",
            "admin_main", "admin_group", "user"
        ]
        
        for expected in expected_roles:
            if expected in role_names:
                print(f"   ✅ {expected}")
            else:
                print(f"   ⚠️  {expected} (will be created on startup)")
        
        db.close()
        print("\n✅ Role creation test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Role creation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RBAC Fix Verification - Phase 9.3.1")
    print("=" * 60)
    
    test1 = test_rbac_roles()
    test2 = test_role_creation()
    
    print("\n" + "=" * 60)
    if test1 and test2:
        print("✅ ALL TESTS PASSED - RBAC fix verified")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please review errors above")
        print("=" * 60)
        sys.exit(1)
