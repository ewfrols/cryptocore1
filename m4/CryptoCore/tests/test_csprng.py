"""
Tests for CSPRNG module (Sprint 3 requirements).
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cryptocore.crypto.csprng import generate_random_bytes


class TestCSPRNG(unittest.TestCase):
    """Test cases for Cryptographically Secure PRNG."""
    
    def test_generate_random_bytes_basic(self):
        """Test basic byte generation with various lengths."""
        test_cases = [1, 16, 32, 64, 128, 256]
        
        for length in test_cases:
            with self.subTest(length=length):
                result = generate_random_bytes(length)
                self.assertEqual(len(result), length)
    
    def test_generate_random_bytes_uniqueness(self):
        """TEST-2: Generate 1000 unique 16-byte keys."""
        num_keys = 1000
        key_set = set()
        
        print(f"\nGenerating {num_keys} random keys for uniqueness test...")
        
        for i in range(num_keys):
            key = generate_random_bytes(16)
            key_hex = key.hex()
            
            # Check for duplicates
            self.assertNotIn(key_hex, key_set,
                           f"Duplicate key found at iteration {i}: {key_hex[:16]}...")
            key_set.add(key_hex)
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1} keys...")
        
        print(f"✓ Successfully generated {len(key_set)} unique 16-byte keys")
        print(f"  No duplicates found")
    
    def test_generate_random_bytes_entropy(self):
        """TEST-4: Basic entropy check - bit distribution."""
        num_samples = 1000
        total_bits = 0
        total_ones = 0
        
        print(f"\nRunning entropy test on {num_samples} samples...")
        
        for i in range(num_samples):
            data = generate_random_bytes(16)
            
            # Count '1' bits
            for byte in data:
                total_ones += bin(byte).count('1')
                total_bits += 8
        
        ones_ratio = total_ones / total_bits
        print(f"  Bit distribution: {ones_ratio:.3%} ones")
        
        # Should be close to 50%
        self.assertGreater(ones_ratio, 0.45,
                          f"Too few ones: {ones_ratio:.3%} (expected ~50%)")
        self.assertLess(ones_ratio, 0.55,
                       f"Too many ones: {ones_ratio:.3%} (expected ~50%)")
        
        print(f"✓ Entropy test passed")
    
    def test_generate_random_bytes_invalid_input(self):
        """Test error handling for invalid inputs."""
        with self.assertRaises(ValueError):
            generate_random_bytes(0)
        
        with self.assertRaises(ValueError):
            generate_random_bytes(-5)
    
    def test_generate_random_bytes_type_error(self):
        """Test error for non-integer input."""
        with self.assertRaises(TypeError):
            generate_random_bytes("16")  # String instead of int


def generate_nist_test_file():
    """
    TEST-3: Generate a file for NIST Statistical Test Suite.
    
    Creates a 10MB file filled with CSPRNG output.
    """
    import time
    
    total_size = 10 * 1024 * 1024  # 10 MB
    output_file = "nist_csprng_test.bin"
    chunk_size = 65536  # 64 KB chunks
    
    print(f"\n{'='*60}")
    print("Generating NIST STS test file")
    print(f"{'='*60}")
    print(f"Size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    print(f"Output: {output_file}")
    
    start_time = time.time()
    bytes_written = 0
    
    try:
        with open(output_file, 'wb') as f:
            while bytes_written < total_size:
                remaining = total_size - bytes_written
                current_chunk = min(chunk_size, remaining)
                
                random_data = generate_random_bytes(current_chunk)
                f.write(random_data)
                bytes_written += len(random_data)
                
                # Progress indicator
                if bytes_written % (1 * 1024 * 1024) == 0:  # Every 1 MB
                    progress = (bytes_written / total_size) * 100
                    elapsed = time.time() - start_time
                    print(f"  Progress: {progress:.1f}% ({bytes_written:,} bytes, "
                          f"{elapsed:.1f}s)")
        
        elapsed = time.time() - start_time
        print(f"\n✓ File generated successfully")
        print(f"  Total bytes: {bytes_written:,}")
        print(f"  Time elapsed: {elapsed:.2f} seconds")
        print(f"  Speed: {bytes_written/elapsed/1024/1024:.2f} MB/s")
        
        # Instructions for NIST STS
        print(f"\n{'='*60}")
        print("NEXT STEPS for NIST STS:")
        print("1. Download NIST STS from:")
        print("   https://csrc.nist.gov/projects/random-bit-generation/documentation-and-software")
        print("2. Compile the tool (if using C version)")
        print("3. Run: ./assess 10000000")
        print("4. When prompted, enter: 0")
        print("5. Enter the file path: {os.path.abspath(output_file)}")
        print("6. Enter: 0 (for all tests)")
        print("7. View results in: experiments/AlgorithmTesting/finalAnalysisReport.txt")
        
        return output_file
        
    except Exception as e:
        print(f"✗ Failed to generate NIST test file: {e}")
        return None


if __name__ == "__main__":
    # Run unit tests
    print("=" * 60)
    print("CSPRNG Module Tests - Sprint 3 Requirements")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    
    # Ask about NIST test file generation
    print("\n" + "=" * 60)
    response = input("\nGenerate 10MB file for NIST STS testing? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        generate_nist_test_file()
    else:
        print("Skipping NIST test file generation.")
        print("You can run it later with:")
        print("  python -c \"from tests.test_csprng import generate_nist_test_file; generate_nist_test_file()\"")