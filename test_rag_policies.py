#!/usr/bin/env python
"""Test RAG system with policy questions"""

import sys
sys.path.insert(0, 'backend')

from rag_engine import RAGEngine

# Load and test RAG
print("=" * 60)
print("Testing RAG System with Updated Policy")
print("=" * 60)
print()

rag = RAGEngine('sk-T4AaQhdHdumu_fBjjE5nyg')
success, msg = rag.load_policy_document('documents/policy.txt')

print(f'✓ Policy Loaded: {success}')
print(f'Status: {msg}')
print()

# Test RAG with policy questions
test_questions = [
    'What is the maternity leave policy?',
    'Are there provisions for menstrual leave?',
    'What childcare support is available?',
    'What are breastfeeding support provisions?',
    'What happens if I experience workplace harassment?'
]

print("=" * 60)
print("Testing RAG Retrieval")
print("=" * 60)
print()

for i, q in enumerate(test_questions, 1):
    print(f"[{i}] Question: {q}")
    result = rag.explain_policy(q)
    print(f"    ✓ Success: {result['success']}")
    if result['success']:
        # Print first 200 chars of explanation
        explanation = result['explanation'][:200] + "..." if len(result['explanation']) > 200 else result['explanation']
        print(f"    Answer: {explanation}")
    print()

print("=" * 60)
print("RAG System Test Complete")
print("=" * 60)
