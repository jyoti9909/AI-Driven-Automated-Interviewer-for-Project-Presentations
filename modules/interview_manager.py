"""
Interview Manager Module
Manages interview flow, conversation state, and follow-up logic
"""

from typing import List, Dict, Optional
from datetime import datetime
from modules.question_generator import QuestionGenerator


class InterviewManager:
    """Manages interview conversation flow"""
    
    def __init__(self, question_generator: QuestionGenerator):
        """
        Initialize interview manager
        
        Args:
            question_generator: QuestionGenerator instance
        """
        self.question_generator = question_generator
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.interview_started = False
        self.interview_completed = False
        self.max_questions = 5
        self.current_question_index = 0
    
    def start_interview(self, context: Dict):
        """
        Start a new interview session
        
        Args:
            context: Initial context with screen_text, speech_text, keywords, etc.
        """
        self.current_context = context
        self.conversation_history = []
        self.interview_started = True
        self.interview_completed = False
        self.current_question_index = 0
        
        # Generate and add first question
        first_q_data = self.question_generator.generate_initial_question(context)
        
        # Handle both Dict and str returns for backward compatibility
        if isinstance(first_q_data, dict):
            first_question = first_q_data['question']
            expected_points = first_q_data.get('expected_points', [])
        else:
            first_question = first_q_data
            expected_points = []
        
        self.conversation_history.append({
            'type': 'question',
            'content': first_question,
            'expected_points': expected_points,
            'timestamp': datetime.now().isoformat(),
            'question_index': 0
        })
    
    def submit_answer(self, answer: str) -> Optional[str]:
        """
        Submit student's answer and get next question
        
        Args:
            answer: Student's answer text
            
        Returns:
            Next question string or None if interview complete
        """
        if not self.interview_started or self.interview_completed:
            return None
        
        # Add answer to history
        self.conversation_history.append({
            'type': 'answer',
            'content': answer,
            'timestamp': datetime.now().isoformat(),
            'question_index': self.current_question_index
        })
        
        # Check if we've reached max questions
        self.current_question_index += 1
        if self.current_question_index >= self.max_questions:
            self.interview_completed = True
            return None
        
        # Generate follow-up question
        last_question = self.conversation_history[-2]['content']  # Previous question
        next_q_data = self.question_generator.generate_followup_question(
            last_question,
            answer,
            self.current_context
        )
        
        # Handle both Dict and str returns for backward compatibility
        if isinstance(next_q_data, dict):
            next_question = next_q_data['question']
            expected_points = next_q_data.get('expected_points', [])
        else:
            next_question = next_q_data
            expected_points = []
        
        # Add question to history
        self.conversation_history.append({
            'type': 'question',
            'content': next_question,
            'expected_points': expected_points,
            'timestamp': datetime.now().isoformat(),
            'question_index': self.current_question_index
        })
        
        return next_question
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
    
    def get_current_question(self) -> Optional[str]:
        """Get the current question being asked"""
        if not self.conversation_history:
            return None
        
        last_item = self.conversation_history[-1]
        if last_item['type'] == 'question':
            return last_item['content']
        return None
    
    def is_complete(self) -> bool:
        """Check if interview is complete"""
        return self.interview_completed
    
    def get_qa_pairs(self) -> List[Dict]:
        """Get question-answer pairs"""
        qa_pairs = []
        current_q = None
        
        for item in self.conversation_history:
            if item['type'] == 'question':
                current_q = item['content']
            elif item['type'] == 'answer' and current_q:
                qa_pairs.append({
                    'question': current_q,
                    'answer': item['content'],
                    'timestamp': item['timestamp']
                })
                current_q = None
        
        return qa_pairs
    
    def reset(self):
        """Reset interview state"""
        self.conversation_history = []
        self.current_context = {}
        self.interview_started = False
        self.interview_completed = False
        self.current_question_index = 0

