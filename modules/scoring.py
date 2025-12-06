"""
Scoring Module
Evaluates interview performance based on rubric
"""

from typing import List, Dict
import re
from difflib import SequenceMatcher


class ScoringSystem:
    """Evaluates interview responses and generates scores"""
    
    def __init__(self):
        """Initialize scoring system with rubric weights"""
        self.rubric = {
            'technical_depth': {
                'weight': 0.30,
                'description': 'How well they explain implementation'
            },
            'clarity': {
                'weight': 0.25,
                'description': 'Structure, vocabulary, confidence'
            },
            'originality': {
                'weight': 0.25,
                'description': 'Uniqueness of design/idea'
            },
            'understanding': {
                'weight': 0.20,
                'description': 'Conceptual grasp'
            }
        }
    
    def evaluate_qa_pair(self, question: str, answer: str, context: Dict, expected_points: List[str] = None) -> Dict:
        """
        Evaluate a single Q&A pair
        
        Args:
            question: Question asked
            answer: Student's answer
            context: Project context (keywords, code snippets, etc.)
            expected_points: List of expected key points in the answer
            
        Returns:
            Dictionary with scores for each criterion and correctness check
        """
        scores = {}
        
        # Technical depth
        scores['technical_depth'] = self._score_technical_depth(answer, context)
        
        # Clarity
        scores['clarity'] = self._score_clarity(answer)
        
        # Originality
        scores['originality'] = self._score_originality(answer, context)
        
        # Understanding
        scores['understanding'] = self._score_understanding(question, answer, context)
        
        # Check answer correctness against expected points
        if expected_points:
            correctness_result = self._check_answer_correctness(answer, expected_points)
            scores['correctness'] = correctness_result
        
        return scores
    
    def _score_technical_depth(self, answer: str, context: Dict) -> float:
        """Score technical depth (0-100)"""
        score = 50  # Base score
        
        answer_lower = answer.lower()
        
        # Technical keywords mentioned
        keywords = context.get('keywords', [])
        mentioned_keywords = sum(1 for kw in keywords if kw.lower() in answer_lower)
        score += min(mentioned_keywords * 5, 20)
        
        # Technical terms
        tech_terms = ['algorithm', 'implementation', 'architecture', 'framework', 
                     'api', 'database', 'optimization', 'performance', 'scalability']
        tech_mentions = sum(1 for term in tech_terms if term in answer_lower)
        score += min(tech_mentions * 5, 15)
        
        # Code references
        code_patterns = ['function', 'class', 'method', 'variable', 'loop', 'condition']
        code_mentions = sum(1 for pattern in code_patterns if pattern in answer_lower)
        score += min(code_mentions * 3, 15)
        
        return min(score, 100)
    
    def _score_clarity(self, answer: str) -> float:
        """Score clarity (0-100)"""
        score = 50  # Base score
        
        # Length check (too short or too long is bad)
        word_count = len(answer.split())
        if 20 <= word_count <= 200:
            score += 20
        elif 10 <= word_count < 20 or 200 < word_count <= 300:
            score += 10
        
        # Sentence structure
        sentences = re.split(r'[.!?]+', answer)
        avg_sentence_length = word_count / max(len(sentences), 1)
        if 10 <= avg_sentence_length <= 25:
            score += 15
        
        # Transition words (indicates structure)
        transitions = ['because', 'however', 'therefore', 'furthermore', 'additionally', 
                      'moreover', 'specifically', 'for example', 'in addition']
        transition_count = sum(1 for trans in transitions if trans in answer.lower())
        score += min(transition_count * 3, 15)
        
        return min(score, 100)
    
    def _score_originality(self, answer: str, context: Dict) -> float:
        """Score originality (0-100)"""
        score = 50  # Base score
        
        answer_lower = answer.lower()
        
        # Unique perspectives
        unique_indicators = ['custom', 'unique', 'novel', 'innovative', 'original', 
                           'different', 'unusual', 'creative', 'personalized']
        unique_count = sum(1 for ind in unique_indicators if ind in answer_lower)
        score += min(unique_count * 8, 30)
        
        # Personal experience mentions
        personal_indicators = ['i', 'my', 'we', 'our', 'experience', 'learned', 'discovered']
        personal_count = sum(1 for ind in personal_indicators if ind in answer_lower)
        score += min(personal_count * 2, 20)
        
        return min(score, 100)
    
    def _score_understanding(self, question: str, answer: str, context: Dict) -> float:
        """Score understanding (0-100)"""
        score = 50  # Base score
        
        answer_lower = answer.lower()
        question_lower = question.lower()
        
        # Answer relevance to question
        question_keywords = set(re.findall(r'\b\w{4,}\b', question_lower))
        answer_keywords = set(re.findall(r'\b\w{4,}\b', answer_lower))
        overlap = len(question_keywords & answer_keywords)
        score += min(overlap * 5, 25)
        
        # Explanation quality indicators
        explanation_indicators = ['explain', 'because', 'reason', 'why', 'how', 
                                'works', 'process', 'step', 'approach']
        explanation_count = sum(1 for ind in explanation_indicators if ind in answer_lower)
        score += min(explanation_count * 3, 25)
        
        return min(score, 100)
    
    def _check_answer_correctness(self, answer: str, expected_points: List[str]) -> Dict:
        """
        Check if answer contains expected key points
        
        Args:
            answer: Student's answer
            expected_points: List of key points that should be mentioned
            
        Returns:
            Dictionary with correctness metrics
        """
        answer_lower = answer.lower()
        
        # Check which expected points are present
        found_points = []
        missing_points = []
        partially_found = []
        
        for point in expected_points:
            point_lower = point.lower()
            
            # Check for exact match (case-insensitive)
            if point_lower in answer_lower:
                found_points.append(point)
            else:
                # Check for partial match using fuzzy matching
                words = point_lower.split()
                word_found_count = sum(1 for word in words if word in answer_lower)
                
                if word_found_count > 0:
                    # If more than 50% of words found, consider it partial
                    if word_found_count / len(words) >= 0.5:
                        partially_found.append(point)
                    else:
                        missing_points.append(point)
                else:
                    # Check for similar words (fuzzy)
                    max_similarity = 0
                    for word in answer_lower.split():
                        if len(word) > 3:  # Only check meaningful words
                            similarity = SequenceMatcher(None, point_lower, word).ratio()
                            max_similarity = max(max_similarity, similarity)
                    
                    if max_similarity > 0.7:  # 70% similarity threshold
                        partially_found.append(point)
                    else:
                        missing_points.append(point)
        
        # Calculate correctness percentage
        total_points = len(expected_points)
        if total_points == 0:
            correctness_percent = 100
        else:
            found_score = len(found_points)
            partial_score = len(partially_found) * 0.5
            correctness_percent = ((found_score + partial_score) / total_points) * 100
        
        return {
            'is_correct': correctness_percent >= 70,  # 70% threshold for "correct"
            'correctness_percent': round(correctness_percent, 1),
            'found_points': found_points,
            'partially_found': partially_found,
            'missing_points': missing_points,
            'total_expected': total_points
        }
    
    def calculate_final_score(self, qa_scores: List[Dict]) -> Dict:
        """
        Calculate final weighted score from all Q&A pairs
        
        Args:
            qa_scores: List of score dictionaries from evaluate_qa_pair
            
        Returns:
            Dictionary with final scores and breakdown
        """
        if not qa_scores:
            return {
                'overall_score': 0,
                'breakdown': {},
                'weighted_scores': {}
            }
        
        # Average scores across all Q&A pairs
        avg_scores = {}
        for criterion in self.rubric.keys():
            criterion_scores = [scores.get(criterion, 0) for scores in qa_scores]
            avg_scores[criterion] = sum(criterion_scores) / len(criterion_scores)
        
        # Calculate weighted overall score
        weighted_scores = {}
        for criterion, data in self.rubric.items():
            weighted_scores[criterion] = avg_scores[criterion] * data['weight']
        
        overall_score = sum(weighted_scores.values())
        
        return {
            'overall_score': round(overall_score, 2),
            'breakdown': avg_scores,
            'weighted_scores': weighted_scores,
            'rubric': self.rubric
        }
    
    def generate_feedback(self, final_scores: Dict, qa_pairs: List[Dict]) -> Dict:
        """
        Generate detailed feedback based on scores
        
        Args:
            final_scores: Output from calculate_final_score
            qa_pairs: List of Q&A pairs
            
        Returns:
            Dictionary with strengths, weaknesses, and suggestions
        """
        breakdown = final_scores['breakdown']
        
        # Identify strengths (scores > 70)
        strengths = []
        for criterion, score in breakdown.items():
            if score >= 70:
                strengths.append({
                    'criterion': criterion.replace('_', ' ').title(),
                    'score': round(score, 1),
                    'description': self.rubric[criterion]['description']
                })
        
        # Identify weaknesses (scores < 60)
        weaknesses = []
        for criterion, score in breakdown.items():
            if score < 60:
                weaknesses.append({
                    'criterion': criterion.replace('_', ' ').title(),
                    'score': round(score, 1),
                    'description': self.rubric[criterion]['description']
                })
        
        # Generate suggestions
        suggestions = []
        for criterion, score in breakdown.items():
            if score < 70:
                if criterion == 'technical_depth':
                    suggestions.append("Try to explain implementation details more thoroughly. Mention specific technologies, algorithms, or design patterns you used.")
                elif criterion == 'clarity':
                    suggestions.append("Work on structuring your explanations better. Use transition words and provide clear examples.")
                elif criterion == 'originality':
                    suggestions.append("Highlight what makes your project unique. Discuss your creative solutions and personal insights.")
                elif criterion == 'understanding':
                    suggestions.append("Demonstrate deeper conceptual understanding by explaining the 'why' behind your decisions, not just the 'what'.")
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions if suggestions else ["Great job overall! Continue building on your strengths."]
        }

