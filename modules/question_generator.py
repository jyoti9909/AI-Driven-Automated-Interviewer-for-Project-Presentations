"""
Question Generator Module
Generates context-aware interview questions using LLM
"""

from typing import List, Dict, Optional
import os
import json

# Try importing LangChain components with fallback
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    try:
        # Newer LangChain versions
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError:
        ChatOpenAI = None
        HumanMessage = None
        SystemMessage = None


class QuestionGenerator:
    """Generates interview questions based on context"""
    
    def __init__(self, use_openai: bool = True, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize question generator
        
        Args:
            use_openai: Whether to use OpenAI API (requires API key)
            model_name: Model name to use
        """
        self.use_openai = use_openai
        self.model_name = model_name
        self.llm = None
        
        if use_openai and ChatOpenAI is not None:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    # Try new API first (model parameter)
                    try:
                        self.llm = ChatOpenAI(
                            model=model_name,
                            temperature=0.7,
                            openai_api_key=api_key
                        )
                    except TypeError:
                        # Fallback to old API (model_name parameter)
                        self.llm = ChatOpenAI(
                            model_name=model_name,
                            temperature=0.7,
                            openai_api_key=api_key
                        )
                except Exception as e:
                    print(f"Error initializing OpenAI: {e}")
                    self.llm = None
                    self.use_openai = False
            else:
                print("Warning: OPENAI_API_KEY not found. Using fallback question generation.")
                self.use_openai = False
        elif use_openai and ChatOpenAI is None:
            print("Warning: LangChain not properly installed. Using fallback question generation.")
            self.use_openai = False
    
    def generate_initial_question(self, context: Dict) -> Dict:
        """
        Generate initial question with expected answer key points
        
        Args:
            context: Dictionary with 'screen_text', 'speech_text', 'keywords', 'code_snippets'
            
        Returns:
            Dictionary with 'question' and 'expected_points'
        """
        screen_text = context.get('screen_text', '')
        speech_text = context.get('speech_text', '')
        keywords = context.get('keywords', [])
        code_snippets = context.get('code_snippets', [])
        
        # Build context summary
        context_summary = f"""
Screen Content: {screen_text[:500]}
Speech Transcript: {speech_text[:500]}
Keywords: {', '.join(keywords[:10])}
Code Snippets: {', '.join(code_snippets[:5])}
"""
        
        if self.llm:
            return self._generate_with_llm(context_summary, is_followup=False, full_context=context)
        else:
            return self._generate_fallback_question(context)
    
    def generate_followup_question(self, previous_question: str, answer: str, context: Dict) -> Dict:
        """
        Generate follow-up question with expected answer key points
        
        Args:
            previous_question: Previous question asked
            answer: Student's answer
            context: Original context
            
        Returns:
            Dictionary with 'question' and 'expected_points'
        """
        qa_context = f"""
Previous Question: {previous_question}
Student's Answer: {answer}
Original Context: {context.get('screen_text', '')[:300]}
"""
        
        if self.llm:
            return self._generate_with_llm(qa_context, is_followup=True, full_context=context)
        else:
            return self._generate_fallback_followup(previous_question, answer)
    
    def _generate_with_llm(self, context: str, is_followup: bool = False, full_context: Dict = None) -> Dict:
        """Generate question with expected answer points using LLM"""
        if self.llm is None or HumanMessage is None or SystemMessage is None:
            return self._generate_fallback_question(full_context or {'screen_text': context})
        
        try:
            if is_followup:
                system_prompt = """You are an expert technical interviewer. Based on the student's answer to the previous question, generate a thoughtful follow-up question WITH expected answer key points.

Return a JSON object with this exact format:
{
    "question": "Your interview question here",
    "expected_points": [
        "Key point 1 that should be in the answer",
        "Key point 2 that should be in the answer",
        "Key point 3 that should be in the answer"
    ]
}

The question should:
1. Probe deeper into their understanding
2. Test knowledge of implementation details
3. Be specific and relevant to their project
4. Be clear and concise

The expected_points should be 3-5 key concepts or terms that a correct answer should mention."""
            else:
                system_prompt = """You are an expert technical interviewer. Based on the project presentation content, generate an insightful initial question WITH expected answer key points.

Return a JSON object with this exact format:
{
    "question": "Your interview question here",
    "expected_points": [
        "Key point 1 that should be in the answer",
        "Key point 2 that should be in the answer",
        "Key point 3 that should be in the answer"
    ]
}

The question should:
1. Test understanding of the project's core concepts
2. Probe technical implementation details
3. Be specific to the content shown
4. Be clear and concise

The expected_points should be 3-5 key concepts or terms that a correct answer should mention."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nGenerate a question with expected answer points:")
            ]
            
            response = self.llm.invoke(messages)
            
            # Handle different response formats
            if hasattr(response, 'content'):
                response_text = response.content.strip()
            elif isinstance(response, str):
                response_text = response.strip()
            else:
                response_text = str(response).strip()
            
            # Try to parse JSON response
            try:
                # Remove markdown code blocks if present
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0].strip()
                
                result = json.loads(response_text)
                return {
                    'question': result.get('question', 'Can you explain your project?'),
                    'expected_points': result.get('expected_points', [])
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, extract question from text
                return {
                    'question': response_text,
                    'expected_points': self._extract_key_points_from_context(full_context or {})
                }
        except Exception as e:
            print(f"Error generating question with LLM: {e}")
            return self._generate_fallback_question(full_context or {'screen_text': context})
    
    def _extract_key_points_from_context(self, context: Dict) -> List[str]:
        """Extract key points from context for expected answers"""
        keywords = context.get('keywords', [])
        code_snippets = context.get('code_snippets', [])
        
        key_points = []
        
        # Add keywords as expected points
        if keywords:
            key_points.extend(keywords[:3])
        
        # Add code snippets
        if code_snippets:
            key_points.extend(code_snippets[:2])
        
        # Add generic tech points if nothing found
        if not key_points:
            key_points = ['implementation details', 'architecture', 'functionality']
        
        return key_points[:5]
    
    def _generate_fallback_question(self, context: Dict) -> Dict:
        """Generate question using rule-based fallback"""
        keywords = context.get('keywords', [])
        code_snippets = context.get('code_snippets', [])
        screen_text = context.get('screen_text', '')
        
        expected_points = self._extract_key_points_from_context(context)
        
        if code_snippets:
            question = f"Can you explain how you implemented {code_snippets[0]} in your project?"
        elif keywords:
            question = f"I noticed you mentioned {keywords[0]}. Can you explain how it's used in your project?"
        elif screen_text:
            question = "Can you walk me through the main components of your project?"
        else:
            question = "Can you explain the core functionality of your project?"
        
        return {
            'question': question,
            'expected_points': expected_points
        }
    
    def _generate_fallback_followup(self, previous_question: str, answer: str) -> Dict:
        """Generate follow-up using rule-based fallback"""
        answer_lower = answer.lower()
        
        # Extract potential key points from answer
        words = [w for w in answer.split() if len(w) > 4]
        expected_points = words[:3] if words else ['details', 'implementation', 'approach']
        
        if any(word in answer_lower for word in ['because', 'since', 'due to']):
            question = "That's interesting. Can you provide a specific example of how that works?"
        elif any(word in answer_lower for word in ['use', 'using', 'utilize']):
            question = "What challenges did you face while implementing that?"
        else:
            question = "Can you elaborate on that point with more technical details?"
        
        return {
            'question': question,
            'expected_points': expected_points
        }

