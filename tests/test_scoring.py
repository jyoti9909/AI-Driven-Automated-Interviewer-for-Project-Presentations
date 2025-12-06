"""
Unit tests for Scoring System
"""

import unittest
from modules.scoring import ScoringSystem


class TestScoringSystem(unittest.TestCase):
    """Test cases for scoring functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scoring = ScoringSystem()
        self.sample_context = {
            'keywords': ['Python', 'Machine Learning', 'TensorFlow'],
            'code_snippets': ['def train_model()', 'import tensorflow']
        }
    
    def test_evaluate_qa_pair(self):
        """Test Q&A pair evaluation"""
        question = "Can you explain your implementation?"
        answer = "I used Python and TensorFlow to build a machine learning model. The implementation includes data preprocessing, model training, and evaluation."
        
        scores = self.scoring.evaluate_qa_pair(question, answer, self.sample_context)
        
        self.assertIn('technical_depth', scores)
        self.assertIn('clarity', scores)
        self.assertIn('originality', scores)
        self.assertIn('understanding', scores)
        
        # Scores should be between 0 and 100
        for score in scores.values():
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
    
    def test_calculate_final_score(self):
        """Test final score calculation"""
        qa_scores = [
            {'technical_depth': 80, 'clarity': 75, 'originality': 70, 'understanding': 85},
            {'technical_depth': 75, 'clarity': 80, 'originality': 75, 'understanding': 80}
        ]
        
        final_scores = self.scoring.calculate_final_score(qa_scores)
        
        self.assertIn('overall_score', final_scores)
        self.assertIn('breakdown', final_scores)
        self.assertIn('weighted_scores', final_scores)
        
        # Overall score should be between 0 and 100
        self.assertGreaterEqual(final_scores['overall_score'], 0)
        self.assertLessEqual(final_scores['overall_score'], 100)
    
    def test_generate_feedback(self):
        """Test feedback generation"""
        final_scores = {
            'overall_score': 75,
            'breakdown': {
                'technical_depth': 80,
                'clarity': 70,
                'originality': 65,
                'understanding': 75
            },
            'rubric': self.scoring.rubric
        }
        
        qa_pairs = [
            {'question': 'Test question', 'answer': 'Test answer'}
        ]
        
        feedback = self.scoring.generate_feedback(final_scores, qa_pairs)
        
        self.assertIn('strengths', feedback)
        self.assertIn('weaknesses', feedback)
        self.assertIn('suggestions', feedback)
        
        self.assertIsInstance(feedback['strengths'], list)
        self.assertIsInstance(feedback['weaknesses'], list)
        self.assertIsInstance(feedback['suggestions'], list)


if __name__ == '__main__':
    unittest.main()

