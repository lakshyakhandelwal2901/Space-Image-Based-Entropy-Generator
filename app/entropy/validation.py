"""Entropy Validation Module - Ensures generated entropy meets quality standards"""

import math
from typing import Dict, List, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class EntropyValidator:
    """Validates entropy quality using statistical tests"""
    
    def __init__(self, min_shannon_entropy: float = 7.8):
        """
        Initialize validator
        
        Args:
            min_shannon_entropy: Minimum acceptable Shannon entropy (bits per byte)
        """
        self.min_shannon_entropy = min_shannon_entropy
    
    def calculate_shannon_entropy(self, data: bytes) -> float:
        """
        Calculate Shannon entropy in bits per byte
        
        Shannon entropy formula: H = -Σ(P(xi) * log2(P(xi)))
        where P(xi) is the probability of byte value xi
        
        Args:
            data: Byte sequence to analyze
            
        Returns:
            Shannon entropy in bits per byte (0.0 to 8.0)
        """
        if not data:
            return 0.0
        
        # Count frequency of each byte value
        byte_counts = Counter(data)
        data_len = len(data)
        
        # Calculate entropy
        entropy = 0.0
        for count in byte_counts.values():
            probability = count / data_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def chi_square_test(self, data: bytes) -> float:
        """
        Chi-square test for uniform distribution
        
        Tests if byte values are uniformly distributed (0-255)
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Chi-square score (0.0 to 1.0, higher is better)
            1.0 = perfectly uniform distribution
        """
        if not data or len(data) < 256:
            return 0.0
        
        # Expected frequency for uniform distribution
        expected_freq = len(data) / 256
        
        # Count actual frequencies
        byte_counts = Counter(data)
        
        # Calculate chi-square statistic
        chi_square = 0.0
        for i in range(256):
            observed = byte_counts.get(i, 0)
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
        
        # Normalize to 0-1 scale (using inverse sigmoid-like function)
        # For truly random data, chi-square should be around 255
        # Score closer to 1.0 means more uniform
        score = 1.0 / (1.0 + abs(chi_square - 255) / 100)
        
        return score
    
    def runs_test(self, data: bytes) -> float:
        """
        Runs test for randomness
        
        Tests for patterns by counting consecutive runs of values
        above/below median
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Runs test score (0.0 to 1.0, higher is better)
        """
        if not data or len(data) < 10:
            return 0.0
        
        # Calculate median
        sorted_data = sorted(data)
        median = sorted_data[len(sorted_data) // 2]
        
        # Convert to sequence of above(1)/below(0) median
        binary_sequence = [1 if b >= median else 0 for b in data]
        
        # Count runs
        runs = 1
        for i in range(1, len(binary_sequence)):
            if binary_sequence[i] != binary_sequence[i-1]:
                runs += 1
        
        # Calculate expected runs for random data
        n1 = sum(binary_sequence)
        n0 = len(binary_sequence) - n1
        
        if n1 == 0 or n0 == 0:
            return 0.0
        
        expected_runs = ((2 * n0 * n1) / (n0 + n1)) + 1
        
        # Calculate variance
        variance = (2 * n0 * n1 * (2 * n0 * n1 - n0 - n1)) / \
                   ((n0 + n1) ** 2 * (n0 + n1 - 1))
        
        if variance == 0:
            return 0.0
        
        # Z-score
        z_score = abs((runs - expected_runs) / math.sqrt(variance))
        
        # Convert z-score to 0-1 scale (closer to 1 is better)
        # Z-score < 2 is generally acceptable
        score = max(0.0, 1.0 - (z_score / 4.0))
        
        return score
    
    def autocorrelation_test(self, data: bytes, lag: int = 1) -> float:
        """
        Test for autocorrelation (self-similarity at different offsets)
        
        Args:
            data: Byte sequence to test
            lag: Offset for correlation check
            
        Returns:
            Autocorrelation score (0.0 to 1.0, higher is better)
            Low correlation indicates good randomness
        """
        if not data or len(data) <= lag:
            return 0.0
        
        # Calculate mean
        mean = sum(data) / len(data)
        
        # Calculate autocorrelation
        numerator = 0.0
        denominator = 0.0
        
        for i in range(len(data) - lag):
            diff1 = data[i] - mean
            diff2 = data[i + lag] - mean
            numerator += diff1 * diff2
            denominator += diff1 ** 2
        
        if denominator == 0:
            return 0.0
        
        correlation = abs(numerator / denominator)
        
        # Score: lower correlation is better
        score = max(0.0, 1.0 - correlation)
        
        return score
    
    def bit_entropy_test(self, data: bytes) -> float:
        """
        Test entropy at the bit level
        
        Checks if individual bits are well-distributed
        
        Args:
            data: Byte sequence to test
            
        Returns:
            Bit-level entropy score (0.0 to 1.0)
        """
        if not data:
            return 0.0
        
        # Count 1s and 0s across all bits
        ones = 0
        total_bits = 0
        
        for byte_val in data:
            for bit_pos in range(8):
                if byte_val & (1 << bit_pos):
                    ones += 1
                total_bits += 1
        
        # Ideal ratio is 0.5 (equal 1s and 0s)
        ratio = ones / total_bits if total_bits > 0 else 0.0
        
        # Score based on deviation from 0.5
        score = 1.0 - abs(ratio - 0.5) * 2
        
        return max(0.0, score)
    
    def validate(self, data: bytes, detailed: bool = False) -> Dict:
        """
        Comprehensive entropy validation
        
        Runs all statistical tests and returns overall quality score
        
        Args:
            data: Byte sequence to validate
            detailed: If True, return detailed test results
            
        Returns:
            Dictionary with validation results
        """
        if not data:
            return {
                'passed': False,
                'quality_score': 0.0,
                'shannon_entropy': 0.0,
                'error': 'Empty data'
            }
        
        # Run all tests
        shannon = self.calculate_shannon_entropy(data)
        chi_square = self.chi_square_test(data)
        runs = self.runs_test(data)
        autocorr = self.autocorrelation_test(data)
        bit_entropy = self.bit_entropy_test(data)
        
        # Calculate overall quality score (weighted average)
        quality_score = (
            shannon / 8.0 * 0.4 +      # 40% weight on Shannon entropy
            chi_square * 0.25 +          # 25% weight on chi-square
            runs * 0.15 +                # 15% weight on runs test
            autocorr * 0.10 +            # 10% weight on autocorrelation
            bit_entropy * 0.10           # 10% weight on bit entropy
        )
        
        # Determine if entropy passes quality threshold
        passed = shannon >= self.min_shannon_entropy and quality_score >= 0.75
        
        result = {
            'passed': passed,
            'quality_score': round(quality_score, 4),
            'shannon_entropy': round(shannon, 4),
            'data_size': len(data)
        }
        
        if detailed:
            result.update({
                'chi_square_score': round(chi_square, 4),
                'runs_test_score': round(runs, 4),
                'autocorrelation_score': round(autocorr, 4),
                'bit_entropy_score': round(bit_entropy, 4),
                'min_required_entropy': self.min_shannon_entropy
            })
        
        logger.debug(f"Entropy validation: Shannon={shannon:.3f}, Quality={quality_score:.3f}, Passed={passed}")
        
        return result
    
    def batch_validate(self, data_blocks: List[bytes]) -> Tuple[List[bytes], List[Dict]]:
        """
        Validate multiple entropy blocks and return only those that pass
        
        Args:
            data_blocks: List of byte sequences to validate
            
        Returns:
            Tuple of (valid_blocks, validation_results)
        """
        valid_blocks = []
        results = []
        
        for block in data_blocks:
            result = self.validate(block)
            results.append(result)
            
            if result['passed']:
                valid_blocks.append(block)
        
        logger.info(f"Batch validation: {len(valid_blocks)}/{len(data_blocks)} blocks passed")
        
        return valid_blocks, results


# Global validator instance
validator = EntropyValidator()


# Utility function for quick validation
def quick_validate(data: bytes) -> bool:
    """
    Quick validation check
    
    Args:
        data: Byte sequence to validate
        
    Returns:
        True if entropy passes quality checks
    """
    result = validator.validate(data)
    return result['passed']


if __name__ == "__main__":
    # Test with various data types
    import os
    
    print("Testing Entropy Validator")
    print("=" * 60)
    
    # Test 1: True random data (from OS)
    true_random = os.urandom(4096)
    result = validator.validate(true_random, detailed=True)
    print("\n1. OS Random Data (4096 bytes):")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Test 2: Predictable data (all zeros)
    zeros = bytes(4096)
    result = validator.validate(zeros, detailed=True)
    print("\n2. All Zeros (4096 bytes):")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Test 3: Repeating pattern
    pattern = bytes([i % 256 for i in range(4096)])
    result = validator.validate(pattern, detailed=True)
    print("\n3. Repeating Pattern (4096 bytes):")
    for key, value in result.items():
        print(f"   {key}: {value}")
    
    # Test 4: Mixed quality
    mixed = os.urandom(2048) + bytes(2048)
    result = validator.validate(mixed, detailed=True)
    print("\n4. Mixed (2048 random + 2048 zeros):")
    for key, value in result.items():
        print(f"   {key}: {value}")
