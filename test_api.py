"""
Test Backend API Endpoints
Run this to verify your backend is working correctly
"""

import requests
import json
from colorama import init, Fore, Style

init(autoreset=True)

API_BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, endpoint, data=None):
    """Test a single API endpoint"""
    print(f"\n{'='*60}")
    print(f"{Fore.CYAN}Testing: {name}{Style.RESET_ALL}")
    print(f"Endpoint: {method} {endpoint}")
    print('='*60)
    
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"\n{Fore.YELLOW}Status Code:{Style.RESET_ALL} {response.status_code}")
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ SUCCESS{Style.RESET_ALL}")
            result = response.json()
            print(f"\n{Fore.YELLOW}Response:{Style.RESET_ALL}")
            print(json.dumps(result, indent=2)[:500] + "...")
            return True
        else:
            print(f"{Fore.RED}✗ FAILED{Style.RESET_ALL}")
            print(f"Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}✗ CONNECTION ERROR{Style.RESET_ALL}")
        print("Backend server is not running!")
        print("\nStart the server with: python backend/main.py")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ ERROR: {str(e)}{Style.RESET_ALL}")
        return False

def main():
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"  Cold Email Generator - API Tests")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    results = []
    
    # Test 1: Root endpoint
    results.append(test_endpoint(
        "Root Endpoint",
        "GET",
        "/"
    ))
    
    # Test 2: Health check
    results.append(test_endpoint(
        "Health Check",
        "GET",
        "/health"
    ))
    
    # Test 3: Job extraction
    sample_job_text = """
    Data Analyst Position at TechCorp
    
    We are looking for an experienced Data Analyst with 3-5 years of experience.
    
    Required Skills:
    - Python programming
    - SQL and database management
    - Data visualization with Tableau or Power BI
    - Statistical analysis
    
    Responsibilities:
    - Analyze business data and create reports
    - Build automated dashboards
    - Work with cross-functional teams
    
    Experience: 3-5 years
    Location: Remote
    """
    
    results.append(test_endpoint(
        "Job Extraction",
        "POST",
        "/api/extract-job",
        {"text": sample_job_text}
    ))
    
    # Test 4: Gmail auth URL
    results.append(test_endpoint(
        "Gmail Auth URL",
        "GET",
        "/api/gmail-auth-url"
    ))
    
    # Summary
    print(f"\n\n{Fore.MAGENTA}{'='*60}")
    print(f"  Test Summary")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {Fore.GREEN}{passed}/{total}{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}✓ All tests passed! Backend is working correctly.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
        print("1. Load extension in Chrome")
        print("2. Connect Gmail account")
        print("3. Start generating cold emails!")
    else:
        print(f"\n{Fore.YELLOW}⚠ Some tests failed. Check the errors above.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Common fixes:{Style.RESET_ALL}")
        print("- Make sure backend server is running")
        print("- Check .env file has GROQ_API_KEY")
        print("- Verify all dependencies are installed")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Tests interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
