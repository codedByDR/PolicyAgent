"""
RAG Engine for Policy Document Analysis
Simplified version using direct OpenAI API calls
"""

import requests
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple


class RAGEngine:
    def __init__(self, api_key: str):
        """Initialize RAG Engine"""
        self.api_key = api_key
        self.base_url = "https://genailab.tcs.in"
        self.policy_chunks = []
        self.policy_text = ""
        
    def load_policy_document(self, document_path: str):
        """Load and process policy document"""
        try:
            with open(document_path, 'r', encoding='utf-8') as f:
                self.policy_text = f.read()
            
            # Split into chunks (simplified)
            self.policy_chunks = self._split_into_chunks(self.policy_text, chunk_size=1000, overlap=200)
            
            return True, "Policy document loaded successfully"
            
        except Exception as e:
            return False, f"Error loading document: {str(e)}"
    
    @staticmethod
    def _split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def _get_relevant_chunks(self, question: str, top_k: int = 3) -> List[str]:
        """Improved retrieval using multiple strategies"""
        if not self.policy_chunks:
            return []
        
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        # Expand question with synonyms and related terms
        synonyms = {
            'childcare': ['childcare', 'child-care', 'child care', 'kids', 'children'],
            'emergency': ['emergency', 'urgent', 'sudden', 'immediate'],
            'maternity': ['maternity', 'pregnancy', 'pregnant', 'birth'],
            'paternity': ['paternity', 'father', 'dad', 'paternal'],
            'adoption': ['adoption', 'adopt', 'adopted'],
            'menstrual': ['menstrual', 'period', 'menstruation'],
            'breastfeeding': ['breastfeeding', 'lactation', 'nursing', 'breast feed'],
            'elder': ['elder', 'elderly', 'aging', 'senior'],
            'fertility': ['fertility', 'ivf', 'infertility', 'conception'],
            'miscarriage': ['miscarriage', 'pregnancy loss', 'stillbirth', 'bereavement'],
            'leave': ['leave', 'absence', 'time off', 'vacation'],
            'days': ['days', 'weeks', 'months', 'duration'],
        }
        
        # Add synonyms to question words
        expanded_words = set(question_words)
        for key, values in synonyms.items():
            if any(key in word or word in key for word in question_words):
                expanded_words.update(values)
        
        chunk_scores = []
        
        for chunk in self.policy_chunks:
            chunk_lower = chunk.lower()
            chunk_words = set(chunk_lower.split())
            
            # Calculate score with expanded words
            score = len(expanded_words & chunk_words)
            
            # Bonus for exact phrase matches
            for key in synonyms:
                if key in question_lower and key in chunk_lower:
                    score += 5
            
            chunk_scores.append((score, chunk))
        
        # Sort by score and return top k
        chunk_scores.sort(reverse=True, key=lambda x: x[0])
        return [chunk for _, chunk in chunk_scores[:top_k] if _ > 0]
    
    def explain_policy(self, question: str) -> dict:
        """Get explanation for policy question using improved RAG"""
        try:
            if not self.policy_chunks:
                return {
                    "success": False,
                    "explanation": "Policy document not loaded. Please load the document first."
                }
            
            # Get more relevant chunks for better context
            relevant_chunks = self._get_relevant_chunks(question, top_k=5)
            
            if not relevant_chunks:
                # If no direct matches, search with broader terms
                relevant_chunks = self.policy_chunks[:3]
            
            context = "\n\n".join(relevant_chunks[:3])
            
            # Create a prompt that ensures complete answers
            prompt = f"""You are an HR policy expert. Answer the question COMPLETELY based ONLY on the policy document below.

POLICY EXCERPT:
{context}

QUESTION: {question}

Instructions:
- Provide a COMPLETE answer that fully addresses the question
- Include SPECIFIC details like number of days/weeks/months when applicable
- If asking about leave policies, always mention the duration in days/weeks/months
- Give a brief description (2-3 sentences) followed by specific details
- Do NOT say "no information" - the policy document contains comprehensive information
- If the exact term isn't found, provide related information from the policy
- Do NOT cut off your answer mid-sentence"""
            
            # Call API with more tokens for complete answers
            response = self._call_llm(prompt, max_tokens=1500)
            
            # Check if response indicates content was blocked, and try local fallback
            if "Content blocked" in response or "safety filters" in response or "rephrasing" in response:
                local_answer = self._get_local_policy_answer(question, relevant_chunks)
                if local_answer:
                    return {
                        "success": True,
                        "explanation": local_answer,
                        "fallback": True
                    }
            
            return {
                "success": True,
                "explanation": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "explanation": f"Error generating explanation: {str(e)}"
            }
    
    def _get_local_policy_answer(self, question: str, chunks: List[str]) -> str:
        """Provide a local answer fallback when AI API blocks content"""
        if not chunks:
            return ""
        
        question_lower = question.lower()
        
        # Key topic patterns to match and provide answers
        topics = {
            'elder': 'elderly care',
            'parent': 'parental',
            'child': 'childcare',
            'matern': 'maternity',
            'patern': 'paternity',
            'adopt': 'adoption',
            'breast': 'breastfeeding',
            'menstrual': 'menstrual',
            'fertility': 'fertility',
            'miscarriage': 'miscarriage',
            'flexible': 'flexible work',
            'remote': 'remote work',
            'hybrid': 'hybrid',
        }
        
        # Find matching topics
        matched_topics = [topic for key, topic in topics.items() if key in question_lower]
        
        if not matched_topics:
            # Return general info from first chunk
            return chunks[0][:800] + "..." if len(chunks[0]) > 800 else chunks[0]
        
        # Search for content related to matched topics
        for chunk in chunks:
            chunk_lower = chunk.lower()
            for topic in matched_topics:
                if topic in chunk_lower:
                    # Found relevant chunk, extract a clean answer
                    lines = chunk.split('\n')
                    relevant_lines = [line for line in lines if topic.lower() in line.lower()]
                    if relevant_lines:
                        return " ".join(relevant_lines[:5])
        
        # Fallback to first chunk
        return chunks[0][:800] + "..." if len(chunks[0]) > 800 else chunks[0]
    
    def get_document_summary(self) -> dict:
        """Get summary of the policy document"""
        try:
            if not self.policy_text:
                return {
                    "success": False,
                    "summary": "Policy document not loaded"
                }
            
            # Check if API key is properly configured (not empty)
            if not self.api_key:
                # Return a local fallback summary based on document content
                return self._get_local_summary()
            
            # Try API call
            policy_preview = self.policy_text[:2500]
            
            prompt = f"""Provide a BRIEF executive summary (3-4 sentences max) of this flexible work and life balance policy. Include key benefits and eligibility.

Policy Document:
{policy_preview}"""
            
            summary = self._call_llm(prompt, max_tokens=300)
            
            # Check if summary contains error message
            if "API key" in summary or "authentication" in summary or "configure" in summary.lower() or "error" in summary.lower():
                # Return local fallback instead
                return self._get_local_summary()
            
            return {
                "success": True,
                "summary": summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "summary": f"Error generating summary: {str(e)}"
            }
    
    def _get_local_summary(self) -> dict:
        """Generate a clean local summary without API calls"""
        if not self.policy_text:
            return {
                "success": False,
                "summary": "Policy document not loaded"
            }
        
        # Extract the EXECUTIVE SUMMARY section (lines 9-23 approximately)
        text = self.policy_text
        
        # Find and extract the executive summary section
        exec_summary_start = text.find("1. EXECUTIVE SUMMARY")
        if exec_summary_start == -1:
            exec_summary_start = text.find("EXECUTIVE SUMMARY")
        
        if exec_summary_start != -1:
            # Find the next section (starts with a number followed by dot)
            next_section = text.find("\n\n=", exec_summary_start + 10)
            if next_section == -1:
                next_section = len(text)
            
            # Extract executive summary
            exec_summary = text[exec_summary_start:next_section].strip()
            
            # Clean up the summary - remove headers and excessive whitespace
            lines = exec_summary.split('\n')
            clean_lines = []
            for line in lines:
                line = line.strip()
                # Skip header lines (containing === or headers)
                if line and not line.startswith('===') and not line.startswith('1. '):
                    clean_lines.append(line)
            
            # Join into a clean paragraph
            summary_text = ' '.join(clean_lines)
            
            # Limit to a reasonable length (around 300 words)
            words = summary_text.split()
            if len(words) > 300:
                summary_text = ' '.join(words[:300]) + '...'
            
            return {
                "success": True,
                "summary": summary_text
            }
        
        # Fallback: Extract first meaningful paragraph
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 100 and not para.startswith('='):
                # Clean it up
                clean = ' '.join(para.split())
                if len(clean) > 500:
                    clean = clean[:500] + '...'
                return {
                    "success": True,
                    "summary": clean
                }
        
        return {
            "success": True,
            "summary": "Flexible Work & Life Balance Policy document is available. Click on 'Ask a Question' to get specific information about the policy."
        }
    
    def _call_llm(self, prompt: str, max_tokens: int = 1500) -> str:
        """Call the LLM API with optimized settings"""
        try:
            # Check if API key is set
            if not self.api_key:
                return "API key not configured. Please set your GenAI Lab API key using the GENAI_API_KEY environment variable or update the API_KEY in backend/app.py"
            
            # Try Bearer token authentication first
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gemini-2.5-pro",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=data,
                verify=False,
                timeout=45
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            elif response.status_code == 403:
                # Check if this is a content moderation block (not authentication issue)
                response_text = response.text.lower()
                if "content blocked" in response_text or "bias_gender" in response_text or "keyword" in response_text:
                    # Extract the blocked keyword for better user feedback
                    try:
                        error_json = response.json()
                        error_msg = error_json.get('error', {}).get('message', '')
                        if isinstance(error_msg, str):
                            # Parse the nested error message
                            import re
                            keyword_match = re.search(r"keyword '(\w+)'", error_msg)
                            category_match = re.search(r"category '(\w+)'", error_msg)
                            keyword = keyword_match.group(1) if keyword_match else "unknown"
                            category = category_match.group(1) if category_match else "unknown"
                            return f"Content blocked by AI safety filters. The keyword '{keyword}' triggered '{category}' category filter. This is not an authentication issue - please try rephrasing your question differently."
                    except:
                        return "Content blocked by AI safety filters. The question may contain sensitive topics. Please try rephrasing your question differently."
                
                # Try alternative authentication - API key header
                headers_alt = {
                    "X-API-Key": self.api_key,
                    "Content-Type": "application/json"
                }
                response_alt = requests.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers_alt,
                    json=data,
                    verify=False,
                    timeout=45
                )
                if response_alt.status_code == 200:
                    result = response_alt.json()
                    return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
                # Check if alternative auth also failed due to content moderation
                if "content blocked" in response_alt.text.lower() or "bias_gender" in response_alt.text.lower():
                    return "Content blocked by AI safety filters. Please try rephrasing your question differently."
                return f"API authentication failed (403). Please check the API key configuration. Response: {response.text[:200]}"
            elif response.status_code == 401:
                return "API key is invalid or expired. Please contact your administrator to get a valid API key."
            else:
                return f"API Error: {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "Unable to connect to AI service. Please check your internet connection and ensure genailab.tcs.in is accessible."
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def close(self):
        """Clean up resources"""
        pass
