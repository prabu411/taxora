#!/usr/bin/env python3
"""
Complete System Test for Taxora AI Finance Assistant
Tests all functionality including new documentation and status pages
"""

import requests
import json
import time

def test_frontend_pages():
    """Test all frontend pages and links."""
    print("🎨 Testing Frontend Pages")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    pages_to_test = [
        ("/static/index.html", "Front Page"),
        ("/static/chat.html", "Chat Interface"),
        ("/docs", "API Documentation"),
        ("/status", "System Status"),
        ("/api/status", "JSON Status API")
    ]
    
    results = {}
    
    for endpoint, name in pages_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working ({response.status_code})")
                results[name] = "✅ Working"
            else:
                print(f"⚠️ {name}: Status {response.status_code}")
                results[name] = f"⚠️ Status {response.status_code}"
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = f"❌ Error: {e}"
    
    return results

def test_api_endpoints():
    """Test core API functionality."""
    print("\n🔗 Testing API Endpoints")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test session creation
        session_response = requests.post(
            f"{base_url}/start",
            json={"name": "Test User", "role": "general"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session Creation: {session_id}")
            
            # Test chat functionality
            chat_response = requests.post(
                f"{base_url}/chat",
                json={
                    "message": "What is budgeting?",
                    "session_id": session_id
                },
                timeout=30
            )
            
            if chat_response.status_code == 200:
                chat_data = chat_response.json()
                reply = chat_data.get("reply", "")
                print(f"✅ Chat Response: {len(reply)} characters")
                print(f"💬 Preview: {reply[:100]}...")
                
                # Test AI provider endpoints
                providers_response = requests.get(f"{base_url}/ai/providers")
                if providers_response.status_code == 200:
                    providers_data = providers_response.json()
                    print(f"✅ AI Providers: {list(providers_data['data']['available_providers'].keys())}")
                else:
                    print(f"⚠️ AI Providers: Status {providers_response.status_code}")
                
                return True
            else:
                print(f"❌ Chat failed: {chat_response.status_code}")
                return False
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        return False

def test_system_status():
    """Test system status and health."""
    print("\n⚡ Testing System Status")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test JSON status
        status_response = requests.get(f"{base_url}/api/status", timeout=10)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ System Status: {status_data.get('system', 'unknown')}")
            print(f"📊 Active Sessions: {status_data.get('active_sessions', 0)}")
            
            services = status_data.get('services', {})
            for service, status in services.items():
                print(f"   • {service}: {status}")
            
            return True
        else:
            print(f"❌ Status check failed: {status_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status Test Error: {e}")
        return False

def test_developer_showcase():
    """Test that developer information is properly displayed."""
    print("\n👨‍💻 Testing Developer Showcase")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        response = requests.get(f"{base_url}/static/index.html", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            developers = ["GaneshPrabu", "EswaraKumar", "Akshya Nethra"]
            roles = ["Lead AI Developer", "Backend Architect", "Frontend Designer"]
            
            all_found = True
            for dev in developers:
                if dev in content:
                    print(f"✅ Developer Found: {dev}")
                else:
                    print(f"❌ Developer Missing: {dev}")
                    all_found = False
            
            for role in roles:
                if role in content:
                    print(f"✅ Role Found: {role}")
                else:
                    print(f"❌ Role Missing: {role}")
                    all_found = False
            
            # Check for IBM Granite
            if "IBM Granite" in content:
                print("✅ IBM Granite branding found")
            else:
                print("❌ IBM Granite branding missing")
                all_found = False
            
            return all_found
        else:
            print(f"❌ Front page failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Developer Showcase Test Error: {e}")
        return False

def main():
    """Run complete system test."""
    print("🚀 TAXORA COMPLETE SYSTEM TEST")
    print("=" * 70)
    
    start_time = time.time()
    
    # Run all tests
    frontend_results = test_frontend_pages()
    api_success = test_api_endpoints()
    status_success = test_system_status()
    developer_success = test_developer_showcase()
    
    # Summary
    print("\n🎉 COMPLETE SYSTEM TEST SUMMARY")
    print("=" * 70)
    
    print("\n📱 Frontend Pages:")
    for page, result in frontend_results.items():
        print(f"   {page}: {result}")
    
    print(f"\n🔗 API Functionality: {'✅ PASS' if api_success else '❌ FAIL'}")
    print(f"⚡ System Status: {'✅ PASS' if status_success else '❌ FAIL'}")
    print(f"👨‍💻 Developer Showcase: {'✅ PASS' if developer_success else '❌ FAIL'}")
    
    # Overall result
    all_frontend_working = all("✅" in result for result in frontend_results.values())
    overall_success = all_frontend_working and api_success and status_success and developer_success
    
    print(f"\n🏆 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_success else '⚠️ SOME ISSUES FOUND'}")
    
    elapsed_time = time.time() - start_time
    print(f"⏱️ Test Duration: {elapsed_time:.2f} seconds")
    
    if overall_success:
        print("\n🎉 CONGRATULATIONS!")
        print("Your Taxora AI Finance Assistant is fully functional with:")
        print("   ✅ Beautiful frontend with developer showcase")
        print("   ✅ Functional API documentation page")
        print("   ✅ Real-time system status monitoring")
        print("   ✅ Complete AI chat functionality")
        print("   ✅ IBM Granite integration properly displayed")
        print("   ✅ All links and pages working correctly")
        
        print("\n🌟 Ready for Production!")
        print("Your system is ready to serve users with:")
        print("   • Professional developer credits")
        print("   • Comprehensive API documentation")
        print("   • Real-time system monitoring")
        print("   • Intelligent AI financial assistance")
        
    else:
        print("\n⚠️ Some issues were found. Please check the details above.")
    
    return overall_success

if __name__ == "__main__":
    main()
