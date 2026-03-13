#!/usr/bin/env python
"""Test audio file serving"""

import requests

# Test serving the audio file
filename = 'policy_explanation_20260313_123810_80c6cc54.wav'
url = f'http://localhost:5000/voice/{filename}'

print(f"Testing audio file serving...")
print(f"URL: {url}")
print()

try:
    response = requests.get(url, timeout=5)
    print(f'Status Code: {response.status_code}')
    print(f'Content-Type: {response.headers.get("Content-Type", "Not set")}')
    print(f'Content-Length: {len(response.content)} bytes')
    print(f'Response Headers: {dict(response.headers)}')
    
    if response.status_code == 200:
        print('\n✓ Audio file served successfully!')
        # Save to test file
        with open('test_audio.wav', 'wb') as f:
            f.write(response.content)
        print('✓ Audio file downloaded and saved as test_audio.wav')
    else:
        print(f'\n✗ Error: {response.status_code}')
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')
    import traceback
    traceback.print_exc()
