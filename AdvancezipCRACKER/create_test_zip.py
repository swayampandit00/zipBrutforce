#!/usr/bin/env python3
"""
Create password-protected ZIP files for testing the ZIP cracker.
"""

import zipfile
import os
import random
import string

def create_test_zip(zip_filename, password, files_to_add=None):
    """Create a password-protected ZIP file with test files"""
    
    if files_to_add is None:
        files_to_add = []
        # Create some test files
        for i in range(3):
            filename = f"test_file_{i}.txt"
            content = f"This is test file {i}\n" + "".join(random.choices(string.ascii_letters + string.digits, k=100))
            
            with open(filename, 'w') as f:
                f.write(content)
            files_to_add.append(filename)
    
    # Create ZIP file with password
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in files_to_add:
            zf.write(filename, arcname=os.path.basename(filename))
            zf.setpassword(password.encode('utf-8'))
    
    # Clean up test files
    for filename in files_to_add:
        if os.path.exists(filename):
            os.remove(filename)
    
    print(f"[*] Created {zip_filename} with password: '{password}'")
    return zip_filename

def main():
    print("Creating test ZIP files for password cracking...")
    
    # Test cases with different password types
    test_cases = [
        ("test_weak.zip", "password"),
        ("test_numbers.zip", "123456"),
        ("test_complex.zip", "P@ssw0rd123"),
        ("test_pattern.zip", "admin2024"),
        ("test_short.zip", "abc"),
        ("test_medium.zip", "monkey123"),
    ]
    
    for zip_file, password in test_cases:
        create_test_zip(zip_file, password)
    
    print("\n[*] Test ZIP files created:")
    for zip_file, _ in test_cases:
        print(f"    - {zip_file}")
    
    print("\n[*] You can now test the ZIP cracker:")
    print("    python zip_cracker.py test_weak.zip -w sample_wordlist.txt")
    print("    python zip_cracker.py test_numbers.zip -b --min-length 6 --max-length 6")
    print("    python zip_cracker.py test_pattern.zip -p word+number")

if __name__ == "__main__":
    main()
