#!/usr/bin/env python3
"""
Comprehensive test script for the /fuse-subtitles endpoint
Tests multiple scenarios including valid requests, authentication, and error handling
"""

import requests
import time
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import sys

class FuseSubtitlesTester:
    def __init__(self):
        self.base_url = "https://smartsub-api-production.up.railway.app"
        self.endpoint = "/fuse-subtitles"
        self.api_key = "sk-smartsub-abc123def456ghi789"
        self.timeout = 60
        
        # File paths relative to the script location
        self.script_dir = Path(__file__).parent
        self.test_files_dir = self.script_dir / "subtitles-fusion-algorithm-public"
        
        # Test file paths
        self.target_srt = self.test_files_dir / "en.srt"
        self.native_srt = self.test_files_dir / "fr.srt"
        self.frequency_list = self.test_files_dir / "frequency-lists" / "fr-5000.txt"
        
        # Validate test files exist
        self._validate_test_files()
    
    def _validate_test_files(self):
        """Validate that all required test files exist"""
        required_files = [self.target_srt, self.native_srt, self.frequency_list]
        missing_files = []
        
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        if missing_files:
            print(f"❌ Missing required test files:")
            for file in missing_files:
                print(f"   - {file}")
            sys.exit(1)
        
        print("✅ All test files found")
    
    def _make_request(self, files: Dict[str, Any], data: Dict[str, Any], 
                     api_key: Optional[str] = None) -> Dict[str, Any]:
        """Make a request to the endpoint and return response details"""
        url = f"{self.base_url}{self.endpoint}"
        
        # Add API key to query parameters
        params = {}
        if api_key:
            params['api_key'] = api_key
        
        start_time = time.time()
        
        try:
            response = requests.post(
                url,
                files=files,
                data=data,
                params=params,
                timeout=self.timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            return {
                'status_code': response.status_code,
                'response_time': response_time,
                'headers': dict(response.headers),
                'content': response.text,
                'success': response.status_code == 200
            }
            
        except requests.exceptions.Timeout:
            return {
                'status_code': None,
                'response_time': self.timeout,
                'headers': {},
                'content': 'Request timed out',
                'success': False,
                'error': 'timeout'
            }
        except requests.exceptions.RequestException as e:
            return {
                'status_code': None,
                'response_time': time.time() - start_time,
                'headers': {},
                'content': str(e),
                'success': False,
                'error': 'request_exception'
            }
    
    def _print_result(self, test_name: str, result: Dict[str, Any]):
        """Print formatted test result"""
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")
        
        if result['success']:
            print(f"✅ Status: SUCCESS")
        else:
            print(f"❌ Status: FAILED")
        
        print(f"⏱️  Response Time: {result['response_time']:.2f} seconds")
        print(f"📊 Status Code: {result['status_code']}")
        
        if 'error' in result:
            print(f"🚨 Error Type: {result['error']}")
        
        # Try to parse JSON response
        try:
            json_content = json.loads(result['content'])
            print(f"📄 Response Content:")
            print(json.dumps(json_content, indent=2))
        except json.JSONDecodeError:
            print(f"📄 Response Content (raw):")
            print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
    
    def test_valid_request(self):
        """Test 1: Valid request with all required files and parameters"""
        print("\n🧪 Running Test 1: Valid Request")
        
        files = {
            'target_srt': open(self.target_srt, 'rb'),
            'native_srt': open(self.native_srt, 'rb'),
            'frequency_list': open(self.frequency_list, 'rb')
        }
        
        data = {
            'target_language': 'en',
            'native_language': 'fr',
            'top_n_words': 2000,
            'enable_inline_translation': False
        }
        
        try:
            result = self._make_request(files, data, self.api_key)
            self._print_result("Valid Request", result)
            
            # Additional validation for successful response
            if result['success']:
                try:
                    json_response = json.loads(result['content'])
                    if 'output_srt' in json_response:
                        output_length = len(json_response['output_srt'])
                        print(f"📝 Output SRT Length: {output_length} characters")
                        
                        # Show first few lines of output
                        output_lines = json_response['output_srt'].split('\n')[:10]
                        print(f"📖 Output Preview (first 10 lines):")
                        for i, line in enumerate(output_lines, 1):
                            print(f"   {i:2d}: {line}")
                        
                        output_lines_count = len(json_response['output_srt'].split('\n'))
                        if output_lines_count > 10:
                            print(f"   ... ({output_lines_count - 10} more lines)")
                    
                    if 'stats' in json_response:
                        print(f"📈 Processing Stats:")
                        for key, value in json_response['stats'].items():
                            print(f"   {key}: {value}")
                            
                except json.JSONDecodeError:
                    print("⚠️  Response is not valid JSON")
            
            return result
            
        finally:
            # Close file handles
            for file_handle in files.values():
                file_handle.close()
    
    def test_invalid_api_key(self):
        """Test 2: Invalid API key (should return 401)"""
        print("\n🧪 Running Test 2: Invalid API Key")
        
        files = {
            'target_srt': open(self.target_srt, 'rb'),
            'native_srt': open(self.native_srt, 'rb'),
            'frequency_list': open(self.frequency_list, 'rb')
        }
        
        data = {
            'target_language': 'en',
            'native_language': 'fr',
            'top_n_words': 2000,
            'enable_inline_translation': False
        }
        
        try:
            result = self._make_request(files, data, "invalid-api-key")
            self._print_result("Invalid API Key", result)
            return result
            
        finally:
            for file_handle in files.values():
                file_handle.close()
    
    def test_missing_api_key(self):
        """Test 3: Missing API key (should return 401)"""
        print("\n🧪 Running Test 3: Missing API Key")
        
        files = {
            'target_srt': open(self.target_srt, 'rb'),
            'native_srt': open(self.native_srt, 'rb'),
            'frequency_list': open(self.frequency_list, 'rb')
        }
        
        data = {
            'target_language': 'en',
            'native_language': 'fr',
            'top_n_words': 2000,
            'enable_inline_translation': False
        }
        
        try:
            result = self._make_request(files, data, None)
            self._print_result("Missing API Key", result)
            return result
            
        finally:
            for file_handle in files.values():
                file_handle.close()
    
    def test_missing_files(self):
        """Test 4: Missing required files (should return 400)"""
        print("\n🧪 Running Test 4: Missing Files")
        
        # Only include target_srt, missing native_srt and frequency_list
        files = {
            'target_srt': open(self.target_srt, 'rb')
        }
        
        data = {
            'target_language': 'en',
            'native_language': 'fr',
            'top_n_words': 2000,
            'enable_inline_translation': False
        }
        
        try:
            result = self._make_request(files, data, self.api_key)
            self._print_result("Missing Files", result)
            return result
            
        finally:
            for file_handle in files.values():
                file_handle.close()
    
    def test_invalid_file_format(self):
        """Test 5: Invalid file format (should return 400)"""
        print("\n🧪 Running Test 5: Invalid File Format")
        
        # Create a temporary invalid file
        invalid_file = self.script_dir / "invalid_file.txt"
        with open(invalid_file, 'w') as f:
            f.write("This is not a valid SRT file")
        
        try:
            files = {
                'target_srt': open(invalid_file, 'rb'),
                'native_srt': open(self.native_srt, 'rb'),
                'frequency_list': open(self.frequency_list, 'rb')
            }
            
            data = {
                'target_language': 'en',
                'native_language': 'fr',
                'top_n_words': 2000,
                'enable_inline_translation': False
            }
            
            result = self._make_request(files, data, self.api_key)
            self._print_result("Invalid File Format", result)
            return result
            
        finally:
            for file_handle in files.values():
                file_handle.close()
            # Clean up temporary file
            if invalid_file.exists():
                invalid_file.unlink()
    
    def test_missing_parameters(self):
        """Test 6: Missing required parameters (should return 400)"""
        print("\n🧪 Running Test 6: Missing Parameters")
        
        files = {
            'target_srt': open(self.target_srt, 'rb'),
            'native_srt': open(self.native_srt, 'rb'),
            'frequency_list': open(self.frequency_list, 'rb')
        }
        
        # Missing required parameters
        data = {
            'target_language': 'en'
            # Missing: native_language, top_n_words, enable_inline_translation
        }
        
        try:
            result = self._make_request(files, data, self.api_key)
            self._print_result("Missing Parameters", result)
            return result
            
        finally:
            for file_handle in files.values():
                file_handle.close()
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("🚀 Starting Comprehensive /fuse-subtitles Endpoint Tests")
        print(f"🎯 Target URL: {self.base_url}{self.endpoint}")
        print(f"🔑 API Key: {self.api_key[:20]}...")
        print(f"⏱️  Timeout: {self.timeout} seconds")
        
        results = {}
        
        # Run all tests
        results['valid_request'] = self.test_valid_request()
        results['invalid_api_key'] = self.test_invalid_api_key()
        results['missing_api_key'] = self.test_missing_api_key()
        results['missing_files'] = self.test_missing_files()
        results['invalid_file_format'] = self.test_invalid_file_format()
        results['missing_parameters'] = self.test_missing_parameters()
        
        # Summary
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print test summary"""
        print(f"\n{'='*60}")
        print("📊 TEST SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📋 Detailed Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title()}: {status} ({result['response_time']:.2f}s)")
        
        # Performance analysis
        response_times = [result['response_time'] for result in results.values() if result['response_time'] is not None]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n⏱️  Performance Analysis:")
            print(f"   Average Response Time: {avg_time:.2f}s")
            print(f"   Fastest Response: {min_time:.2f}s")
            print(f"   Slowest Response: {max_time:.2f}s")
            
            if max_time > 30:
                print(f"   ⚠️  Warning: Some responses exceeded 30 seconds")

def main():
    """Main function to run the tests"""
    try:
        tester = FuseSubtitlesTester()
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        all_passed = all(result['success'] for result in results.values())
        sys.exit(0 if all_passed else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
