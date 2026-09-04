#%%

#!/usr/bin/env python3
"""
Caesar Cipher - Professional Edition
Enhanced with encryption, decryption, brute-force analysis, and frequency analysis.

Features:
- Caesar cipher encryption/decryption with configurable shift
- Brute-force decryption (try all 26 shifts)
- Frequency analysis (letter frequency distribution)
- Word-matching against common English words
- Chi-squared frequency test
- Educational analysis mode
- Supports Jupyter and terminal

Usage:
    # Terminal:
    python caesar_cipher_pro.py
    
    # Import:
    from caesar_cipher_pro import encrypt, decrypt, brute_force_decrypt
"""

import sys
import re
from typing import Dict, List, Tuple, Any
from collections import Counter
import math


# ============================================================================
# CONFIGURATION & DATA
# ============================================================================

# English letter frequency distribution (%)
ENGLISH_FREQUENCIES = {
    'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
    's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
    'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
    'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

# Common English words (sample dictionary)
COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know",
    "take", "people", "into", "year", "your", "good", "some", "could",
    "them", "see", "other", "than", "then", "now", "look", "only", "come",
    "its", "over", "think", "also", "back", "after", "use", "two", "how",
    "our", "work", "first", "well", "way", "even", "new", "want", "because",
    "any", "these", "give", "day", "most", "us", "is", "was", "are", "been",
    "has", "had", "having", "do", "does", "doing", "did", "should", "may",
    "might", "must", "can", "could", "shall", "world", "right", "hand",
    "life", "part", "place", "hand", "case", "week", "number", "high",
    "group", "long", "same", "different", "letter", "often", "each",
}


# ============================================================================
# ENCRYPTION/DECRYPTION FUNCTIONS
# ============================================================================

def encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt text using Caesar cipher.
    
    Args:
        plaintext: Text to encrypt
        shift: Shift value (1-25)
    
    Returns:
        Encrypted ciphertext
    """
    ciphertext = ""
    
    for char in plaintext:
        if char.isalpha():
            # Determine if uppercase or lowercase
            start = ord('A') if char.isupper() else ord('a')
            # Apply shift within alphabet range
            shifted = (ord(char) - start + shift) % 26
            ciphertext += chr(start + shifted)
        else:
            # Keep non-alphabetic characters unchanged
            ciphertext += char
    
    return ciphertext


def decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt text encrypted with Caesar cipher.
    
    Args:
        ciphertext: Text to decrypt
        shift: Original shift value used in encryption
    
    Returns:
        Decrypted plaintext
    """
    # Decryption is encryption with negative shift
    return encrypt(ciphertext, -shift)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_frequency(text: str) -> Dict[str, float]:
    """
    Calculate letter frequency distribution (%).
    
    Args:
        text: Text to analyze
    
    Returns:
        Dictionary with letter frequencies as percentages
    """
    # Extract only letters
    letters = [char.lower() for char in text if char.isalpha()]
    
    if not letters:
        return {}
    
    # Count occurrences
    counts = Counter(letters)
    total = len(letters)
    
    # Convert to percentages
    frequencies = {letter: (count / total) * 100 for letter, count in counts.items()}
    
    return frequencies


def chi_squared_score(text: str) -> float:
    """
    Calculate chi-squared score comparing text frequency to English.
    Lower score = more likely English (better plaintext candidate).
    
    Args:
        text: Text to analyze
    
    Returns:
        Chi-squared score
    """
    observed_freq = calculate_frequency(text)
    chi_sq = 0.0
    
    for letter in ENGLISH_FREQUENCIES:
        observed = observed_freq.get(letter, 0)
        expected = ENGLISH_FREQUENCIES[letter]
        
        if expected > 0:
            chi_sq += ((observed - expected) ** 2) / expected
    
    return chi_sq


def count_words_in_text(text: str) -> Tuple[int, int, float]:
    """
    Count how many words from dictionary appear in text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (word_count, total_words, percentage)
    """
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return 0, 0, 0.0
    
    matched_words = sum(1 for word in words if word in COMMON_WORDS)
    percentage = (matched_words / len(words)) * 100
    
    return matched_words, len(words), percentage


# ============================================================================
# BRUTE-FORCE & ANALYSIS FUNCTIONS
# ============================================================================

def brute_force_decrypt(ciphertext: str, show_all: bool = False) -> Dict[int, Dict[str, Any]]:
    """
    Try all 26 possible shifts and score results.
    
    Args:
        ciphertext: Encrypted text
        show_all: If True, show all shifts; otherwise show top 5
    
    Returns:
        Dictionary of shifts with analysis scores
    """
    results = {}
    
    for shift in range(26):
        decrypted = decrypt(ciphertext, shift)
        
        # Calculate scoring metrics
        chi_sq = chi_squared_score(decrypted)
        matched_words, total_words, word_percentage = count_words_in_text(decrypted)
        
        # Combined score (lower chi_squared + higher word match = better)
        # Normalize scores for fair comparison
        score = (100 - chi_sq) + word_percentage
        
        results[shift] = {
            'decrypted': decrypted,
            'chi_squared': round(chi_sq, 2),
            'matched_words': matched_words,
            'total_words': total_words,
            'word_percentage': round(word_percentage, 1),
            'combined_score': round(score, 2),
            'confidence': "HIGH" if chi_sq < 100 and word_percentage > 30 else "MEDIUM" if chi_sq < 200 else "LOW"
        }
    
    return results


def analyze_cipher(ciphertext: str, plaintext: str = None) -> Dict[str, Any]:
    """
    Comprehensive analysis of ciphertext.
    
    Args:
        ciphertext: Encrypted text
        plaintext: Optional plaintext for comparison
    
    Returns:
        Analysis dictionary
    """
    analysis = {
        'ciphertext_length': len(ciphertext),
        'letter_count': sum(1 for c in ciphertext if c.isalpha()),
        'space_count': ciphertext.count(' '),
        'frequency': calculate_frequency(ciphertext),
        'unique_letters': len(set(c.lower() for c in ciphertext if c.isalpha())),
    }
    
    if plaintext:
        analysis['plaintext_length'] = len(plaintext)
        analysis['plaintext_letters'] = sum(1 for c in plaintext if c.isalpha())
        analysis['plaintext_frequency'] = calculate_frequency(plaintext)
        analysis['match_percentage'] = round(
            (sum(1 for a, b in zip(ciphertext.lower(), plaintext.lower()) if a == b) / len(plaintext)) * 100,
            1
        ) if len(plaintext) > 0 else 0
    
    return analysis


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_encryption_result(plaintext: str, ciphertext: str, shift: int) -> None:
    """Display encryption result."""
    print("\n" + "=" * 70)
    print("CAESAR CIPHER - ENCRYPTION RESULT")
    print("=" * 70)
    print(f"\nShift Value: {shift}")
    print(f"Plaintext:   {plaintext}")
    print(f"Ciphertext:  {ciphertext}")
    print(f"Length:      {len(plaintext)} characters")
    
    # Show frequency comparison
    plain_freq = calculate_frequency(plaintext)
    cipher_freq = calculate_frequency(ciphertext)
    
    print("\n" + "-" * 70)
    print("FREQUENCY ANALYSIS")
    print("-" * 70)
    print("Top 5 letters (Plaintext):  ", sorted(plain_freq.items(), key=lambda x: x[1], reverse=True)[:5])
    print("Top 5 letters (Ciphertext): ", sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)[:5])
    print("=" * 70)


def display_brute_force_results(results: Dict[int, Dict[str, Any]], top_n: int = 5) -> None:
    """Display brute-force decryption results."""
    print("\n" + "=" * 70)
    print("CAESAR CIPHER - BRUTE-FORCE DECRYPTION")
    print("=" * 70)
    
    # Sort by combined score (descending)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['combined_score'], reverse=True)
    
    print(f"\nShowing top {min(top_n, len(sorted_results))} results (scored by English likelihood):\n")
    print(f"{'Shift':<6} {'Confidence':<12} {'Score':<8} {'Chi²':<8} {'Words':<8} {'Decrypted Text (first 50 chars)':<50}")
    print("-" * 120)
    
    for rank, (shift, result) in enumerate(sorted_results[:top_n], 1):
        text_preview = result['decrypted'][:50].replace('\n', ' ') + "..." if len(result['decrypted']) > 50 else result['decrypted']
        print(f"{shift:<6} {result['confidence']:<12} {result['combined_score']:<8} {result['chi_squared']:<8} "
              f"{result['word_percentage']:<8}% {text_preview:<50}")
    
    print("\n" + "-" * 70)
    print("LEGEND:")
    print("  Shift:      Caesar shift value (0-25)")
    print("  Confidence: Likelihood this is correct English based on letter frequency")
    print("  Score:      Higher = more likely English")
    print("  Chi²:       Chi-squared test (lower = better match to English)")
    print("  Words:      Percentage of recognized English words")
    print("=" * 70)


def display_detailed_analysis(shift: int, result: Dict[str, Any]) -> None:
    """Display detailed analysis of a specific shift result."""
    print("\n" + "=" * 70)
    print(f"DETAILED ANALYSIS - SHIFT {shift}")
    print("=" * 70)
    
    print(f"\nDecrypted text:\n{result['decrypted']}\n")
    print(f"Confidence:        {result['confidence']}")
    print(f"Combined Score:    {result['combined_score']}")
    print(f"Chi-Squared Test:  {result['chi_squared']}")
    print(f"Matched Words:     {result['matched_words']} / {result['total_words']} ({result['word_percentage']}%)")
    print("=" * 70)


# ============================================================================
# INTERACTIVE FUNCTIONS
# ============================================================================

def interactive_menu() -> int:
    """Display menu and return user choice."""
    print("\n" + "-" * 70)
    print("OPTIONS:")
    print("-" * 70)
    print("  1. Encrypt text (with known shift)")
    print("  2. Decrypt text (with known shift)")
    print("  3. Brute-force decrypt (try all shifts)")
    print("  4. Analyze ciphertext")
    print("  5. Educational mode (guided analysis)")
    print("  6. Exit")
    print("-" * 70)
    
    choice = input("\nSelect option (1-6): ").strip()
    return choice


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main function - interactive Caesar cipher tool."""
    print("=" * 70)
    print("CAESAR CIPHER - PROFESSIONAL EDITION")
    print("=" * 70)
    print("\nThis tool demonstrates Caesar cipher encryption with:")
    print("  • Encryption/decryption with configurable shift")
    print("  • Brute-force decryption (all 26 shifts)")
    print("  • Frequency analysis (letter distribution)")
    print("  • Chi-squared English likelihood test")
    print("  • Dictionary word matching")
    print("  • Educational mode")
    
    while True:
        choice = interactive_menu()
        
        if choice == '1':
            # Encrypt
            plaintext = input("\nEnter text to encrypt: ").strip()
            if not plaintext:
                print("Error: Text cannot be empty")
                continue
            
            try:
                shift = int(input("Enter shift value (0-25): ").strip())
                if 0 <= shift <= 25:
                    ciphertext = encrypt(plaintext, shift)
                    display_encryption_result(plaintext, ciphertext, shift)
                else:
                    print("Error: Shift must be between 0 and 25")
            except ValueError:
                print("Error: Please enter a valid number")
        
        elif choice == '2':
            # Decrypt
            ciphertext = input("\nEnter text to decrypt: ").strip()
            if not ciphertext:
                print("Error: Text cannot be empty")
                continue
            
            try:
                shift = int(input("Enter shift value (0-25): ").strip())
                if 0 <= shift <= 25:
                    plaintext = decrypt(ciphertext, shift)
                    print(f"\nDecrypted text: {plaintext}")
                else:
                    print("Error: Shift must be between 0 and 25")
            except ValueError:
                print("Error: Please enter a valid number")
        
        elif choice == '3':
            # Brute-force
            ciphertext = input("\nEnter ciphertext to crack: ").strip()
            if not ciphertext:
                print("Error: Text cannot be empty")
                continue
            
            results = brute_force_decrypt(ciphertext)
            display_brute_force_results(results, top_n=5)
            
            # Allow user to examine top result
            show_detail = input("\nView detailed analysis of top result? (y/n): ").strip().lower()
            if show_detail == 'y':
                top_shift = max(results.items(), key=lambda x: x[1]['combined_score'])[0]
                display_detailed_analysis(top_shift, results[top_shift])
        
        elif choice == '4':
            # Analyze
            ciphertext = input("\nEnter ciphertext to analyze: ").strip()
            if not ciphertext:
                print("Error: Text cannot be empty")
                continue
            
            analysis = analyze_cipher(ciphertext)
            print("\n" + "=" * 70)
            print("CIPHERTEXT ANALYSIS")
            print("=" * 70)
            print(f"Length:          {analysis['ciphertext_length']} characters")
            print(f"Letters:         {analysis['letter_count']}")
            print(f"Spaces:          {analysis['space_count']}")
            print(f"Unique letters:  {analysis['unique_letters']} / 26")
            
            if analysis['frequency']:
                sorted_freq = sorted(analysis['frequency'].items(), key=lambda x: x[1], reverse=True)
                print("\nFrequency distribution (top 10):")
                for letter, freq in sorted_freq[:10]:
                    bar = "█" * int(freq / 2)
                    print(f"  {letter.upper()}: {bar} {freq:.1f}%")
            print("=" * 70)
        
        elif choice == '5':
            # Educational mode
            print("\n" + "=" * 70)
            print("EDUCATIONAL MODE")
            print("=" * 70)
            
            example_text = "HELLO WORLD"
            example_shift = 3
            encrypted = encrypt(example_text, example_shift)
            
            print(f"\nExample: '{example_text}' with shift {example_shift}")
            print(f"Encrypted: '{encrypted}'")
            print("\nHow it works:")
            print(f"  H (position 7) + {example_shift} = K (position 10)")
            print(f"  E (position 4) + {example_shift} = H (position 7)")
            print(f"  ... and so on")
            
            print("\nWhy Caesar cipher is weak:")
            print("  1. Only 26 possible shifts")
            print("  2. Letter frequency is preserved")
            print("  3. Easy brute-force attack")
            print("  4. No key - just the shift value")
            
            print("\nFrequency analysis advantage:")
            print("  In English, 'E' is most common (~12.7%)")
            print("  If 'K' appears most in ciphertext, shift is likely 3")
            print("=" * 70)
        
        elif choice == '6':
            print("\nGoodbye! 🔐")
            break
        
        else:
            print("Invalid option. Please choose 1-6.")
        
        # Ask to continue
        if choice in ['1', '2', '3', '4', '5']:
            again = input("\nContinue? (y/n): ").strip().lower()
            if again != 'y':
                print("\nGoodbye! 🔐")
                break
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 🔐")
        sys.exit(0)
