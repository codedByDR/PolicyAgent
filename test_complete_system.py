#!/usr/bin/env python
"""Test complete system: RAG + Voice"""

import requests
import json
import time

API_URL = "http://localhost:5000/api"

print("=" * 70)
print("TESTING: AI Assistance with RAG + Voice Generation")
print("=" * 70)
print()

# Test questions about women-specific policies
test_cases = [
    {
        "question": "What is the maternity leave policy?",
        "language": "en"
    },
    {
        "question": "What are the breastfeeding support provisions?",
        "language": "en"
    },
    {
        "question": "Is there any support for childcare costs?",
        "language": "en"
    }
]

for idx, test in enumerate(test_cases, 1):
    print(f"\n[Test {idx}] Question: {test['question']}")
    print("-" * 70)
    
    # Step 1: Get AI Answer using RAG
    print("Step 1: Retrieving answer from RAG system...")
    response = requests.post(
        f"{API_URL}/explain",
        json={"question": test['question']},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            answer = result['explanation']
            print(f"✓ RAG Answer: {answer[:150]}...")
            
            # Step 2: Generate Voice Note
            print(f"\nStep 2: Generating voice note ({test['language']})...")
            voice_response = requests.post(
                f"{API_URL}/voice",
                json={"text": answer, "language": test['language']},
                timeout=30
            )
            
            if voice_response.status_code == 200:
                voice_result = voice_response.json()
                if voice_result['success']:
                    print(f"✓ Voice Generated: {voice_result['filename']}")
                    print(f"  Language: {voice_result['language']}")
                    print(f"  File Size: {voice_result.get('file_path', 'N/A')}")
                else:
                    print(f"✗ Voice Error: {voice_result.get('message')}")
            else:
                print(f"✗ Voice API Error: {voice_response.status_code}")
        else:
            print(f"✗ RAG Error: {result.get('explanation')}")
    else:
        print(f"✗ API Error: {response.status_code}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
