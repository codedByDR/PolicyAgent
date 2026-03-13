#!/usr/bin/env python
"""Test voice generation endpoint"""

import requests
import json
import sys

url = 'http://localhost:5000/api/voice'
data = {
    'text': 'This is a test of the maternity leave policy. Employees are entitled to three months of fully paid maternity leave plus flexible return to work arrangements.',
    'language': 'en'
}

print("Testing voice generation endpoint...")
print(f"Text: {data['text'][:50]}...")
print(f"Language: {data['language']}")
print()

try:
    response = requests.post(url, json=data, timeout=30)
    print(f"Status: {response.status_code}")
    
    result = response.json()
    print("Response:")
    print(json.dumps(result, indent=2))
    
    if result.get('success') and result.get('filename'):
        print(f"\n✓ Audio file created: {result['filename']}")
        print(f"file_path: {result.get('file_path')}")
    else:
        print(f"\n✗ Generation failed: {result.get('message')}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
