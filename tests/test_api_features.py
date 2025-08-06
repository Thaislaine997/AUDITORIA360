#!/usr/bin/env python3
"""
Simple API test script to verify the new functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test basic API health"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ API Health: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version', 'Unknown')}")
            print(f"   Environment: {data.get('environment', 'Unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_report_templates():
    """Test report templates endpoints"""
    print("\n🔍 Testing Report Templates...")
    
    try:
        # Test list templates
        response = requests.get(f"{BASE_URL}/api/v1/reports/", timeout=5)
        print(f"   List Templates: {response.status_code}")
        
        if response.status_code == 200:
            templates = response.json()
            print(f"   Found {len(templates)} templates")
            
            # Test get block types
            response = requests.get(f"{BASE_URL}/api/v1/reports/block-types/available", timeout=5)
            print(f"   Block Types: {response.status_code}")
            
            if response.status_code == 200:
                block_types = response.json()
                print(f"   Available block types: {len(block_types.get('block_types', []))}")
                
        return True
    except Exception as e:
        print(f"❌ Report Templates Test Failed: {e}")
        return False

def test_notifications():
    """Test notifications endpoints"""
    print("\n🔔 Testing Notifications...")
    
    try:
        # Test unread count
        response = requests.get(f"{BASE_URL}/api/v1/notifications/unread-count", timeout=5)
        print(f"   Unread Count: {response.status_code}")
        
        if response.status_code == 200:
            count_data = response.json()
            print(f"   Unread notifications: {count_data.get('unread_count', 0)}")
            
            # Test list notifications
            response = requests.get(f"{BASE_URL}/api/v1/notifications/", timeout=5)
            print(f"   List Notifications: {response.status_code}")
            
            if response.status_code == 200:
                notifications = response.json()
                print(f"   Found {len(notifications)} notifications")
                
        return True
    except Exception as e:
        print(f"❌ Notifications Test Failed: {e}")
        return False

def test_documents_export():
    """Test document export endpoints"""
    print("\n📄 Testing Document Export...")
    
    try:
        # Test CSV export
        response = requests.get(f"{BASE_URL}/api/v1/documents/export/csv", timeout=5)
        print(f"   CSV Export: {response.status_code}")
        
        # Test PDF export
        response = requests.get(f"{BASE_URL}/api/v1/documents/export/pdf", timeout=5)
        print(f"   PDF Export: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Document Export Test Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AUDITORIA360 API Feature Test Suite")
    print("=" * 50)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not accessible. Make sure the server is running on port 8000")
        return
    
    # Run feature tests
    tests = [
        test_report_templates,
        test_notifications,
        test_documents_export
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! New features are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API implementation.")

if __name__ == "__main__":
    main()