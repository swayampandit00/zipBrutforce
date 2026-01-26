#!/usr/bin/env python3
"""
ZIP Password Cracker
Supports dictionary attacks, brute force attacks, and pattern-based password generation.
"""

import zipfile
import argparse
import itertools
import string
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import multiprocessing

class ZipCracker:
    def __init__(self, zip_file, verbose=False):
        self.zip_file = zip_file
        self.verbose = verbose
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.lock = Lock()
        
        # Validate ZIP file
        if not os.path.exists(zip_file):
            raise FileNotFoundError(f"ZIP file not found: {zip_file}")
        
        try:
            with zipfile.ZipFile(zip_file, 'r') as zf:
                if len(zf.namelist()) == 0:
                    raise ValueError("ZIP file is empty")
        except zipfile.BadZipFile:
            raise ValueError("Invalid ZIP file format")
    
    def test_password(self, password):
        """Test if password can extract the ZIP file"""
        try:
            with zipfile.ZipFile(self.zip_file, 'r') as zf:
                # Try to extract the first file to test password
                first_file = zf.namelist()[0]
                zf.extract(first_file, pwd=password.encode('utf-8'))
            return True
        except (zipfile.BadZipFile, RuntimeError, KeyError) as e:
            if self.verbose:
                print(f"[*] Failed password '{password}': {str(e)[:50]}")
            return False
        except Exception as e:
            if self.verbose:
                print(f"[*] Error with password '{password}': {str(e)[:50]}")
            return False
    
    def dictionary_attack(self, wordlist, max_workers=None):
        """Dictionary attack using a wordlist"""
        if not os.path.exists(wordlist):
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")
        
        print(f"[*] Starting dictionary attack with {wordlist}")
        print(f"[*] Using {max_workers or multiprocessing.cpu_count()} workers")
        
        self.start_time = time.time()
        
        with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
        
        total_passwords = len(passwords)
        print(f"[*] Loaded {total_passwords:,} passwords")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._test_password_worker, pwd): pwd for pwd in passwords}
            
            for i, future in enumerate(as_completed(futures), 1):
                if self.found_password:
                    break
                
                password = futures[future]
                try:
                    if future.result():
                        self.found_password = password
                        print(f"\n[+] PASSWORD FOUND: {password}")
                        return password
                except Exception:
                    pass
                
                # Progress update
                if i % 1000 == 0 or i == total_passwords:
                    elapsed = time.time() - self.start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    print(f"\r[*] Tried {i:,}/{total_passwords:,} passwords ({rate:.1f} pwd/s)", end='', flush=True)
        
        print(f"\n[-] Password not found in wordlist")
        return None
    
    def _test_password_worker(self, password):
        """Worker function for thread pool"""
        if self.found_password:
            return False
        
        with self.lock:
            self.attempts += 1
        
        if self.verbose and self.attempts % 10000 == 0:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            print(f"[*] Attempts: {self.attempts:,} ({rate:.1f} pwd/s)")
        
        return self.test_password(password)
    
    def brute_force_attack(self, min_length=1, max_length=6, charset=None, max_workers=None):
        """Brute force attack with configurable character set and length"""
        if charset is None:
            charset = string.ascii_lowercase + string.digits
        
        print(f"[*] Starting brute force attack")
        print(f"[*] Character set: {charset}")
        print(f"[*] Password length: {min_length}-{max_length}")
        print(f"[*] Using {max_workers or multiprocessing.cpu_count()} workers")
        
        self.start_time = time.time()
        
        # Calculate total combinations for progress tracking
        total_combinations = sum(len(charset) ** length for length in range(min_length, max_length + 1))
        print(f"[*] Total combinations to try: {total_combinations:,}")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for length in range(min_length, max_length + 1):
                print(f"[*] Trying length {length}...")
                
                for attempt in itertools.product(charset, repeat=length):
                    if self.found_password:
                        break
                    
                    password = ''.join(attempt)
                    future = executor.submit(self._test_password_worker, password)
                    futures.append(future)
                    
                    # Limit futures to prevent memory issues
                    if len(futures) > 10000:
                        for f in as_completed(futures):
                            if self.found_password:
                                break
                        futures = []
                
                # Check if password found for this length
                if self.found_password:
                    break
        
        if self.found_password:
            print(f"\n[+] PASSWORD FOUND: {self.found_password}")
        else:
            print(f"\n[-] Password not found in brute force range")
        
        return self.found_password
    
    def pattern_attack(self, patterns, max_workers=None):
        """Attack using common password patterns"""
        print(f"[*] Starting pattern-based attack")
        print(f"[*] Using {max_workers or multiprocessing.cpu_count()} workers")
        
        self.start_time = time.time()
        passwords = self._generate_pattern_passwords(patterns)
        
        print(f"[*] Generated {len(passwords):,} pattern-based passwords")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self._test_password_worker, pwd): pwd for pwd in passwords}
            
            for i, future in enumerate(as_completed(futures), 1):
                if self.found_password:
                    break
                
                password = futures[future]
                try:
                    if future.result():
                        self.found_password = password
                        print(f"\n[+] PASSWORD FOUND: {password}")
                        return password
                except Exception:
                    pass
                
                if i % 1000 == 0:
                    elapsed = time.time() - self.start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    print(f"\r[*] Tried {i:,} passwords ({rate:.1f} pwd/s)", end='', flush=True)
        
        print(f"\n[-] Password not found in patterns")
        return None
    
    def _generate_pattern_passwords(self, patterns):
        """Generate passwords based on common patterns"""
        passwords = set()
        
        # Common base words
        base_words = ['password', 'admin', 'user', 'login', 'test', 'demo', '123', 'qwerty', 'abc']
        
        # Common numbers
        numbers = ['123', '1234', '12345', '2023', '2024', '2025', '001', '002', '999', '000']
        
        # Common symbols
        symbols = ['!', '@', '#', '$', '%', '&', '*']
        
        for pattern in patterns:
            if pattern == 'word+number':
                for word in base_words:
                    for num in numbers:
                        passwords.add(word + num)
                        passwords.add(num + word)
            
            elif pattern == 'word+symbol':
                for word in base_words:
                    for sym in symbols:
                        passwords.add(word + sym)
                        passwords.add(sym + word)
            
            elif pattern == 'capitalized':
                for word in base_words:
                    passwords.add(word.capitalize())
                    passwords.add(word.upper())
            
            elif pattern == 'leet':
                leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
                for word in base_words:
                    leet_word = ''.join(leet_map.get(c.lower(), c) for c in word)
                    passwords.add(leet_word)
        
        return list(passwords)
    
    def get_stats(self):
        """Get cracking statistics"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            return {
                'attempts': self.attempts,
                'elapsed_time': elapsed,
                'rate': rate,
                'password_found': self.found_password
            }
        return None


def main():
    parser = argparse.ArgumentParser(description='ZIP Password Cracker')
    parser.add_argument('zip_file', help='Path to the ZIP file')
    parser.add_argument('-w', '--wordlist', help='Path to wordlist file')
    parser.add_argument('-b', '--brute', action='store_true', help='Use brute force attack')
    parser.add_argument('-p', '--patterns', nargs='+', 
                       choices=['word+number', 'word+symbol', 'capitalized', 'leet'],
                       help='Use pattern-based attack')
    parser.add_argument('--min-length', type=int, default=1, help='Minimum password length for brute force')
    parser.add_argument('--max-length', type=int, default=6, help='Maximum password length for brute force')
    parser.add_argument('--charset', help='Character set for brute force (default: lowercase+digits)')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    try:
        cracker = ZipCracker(args.zip_file, args.verbose)
        
        if args.wordlist:
            result = cracker.dictionary_attack(args.wordlist, args.threads)
        elif args.brute:
            charset = args.charset or string.ascii_lowercase + string.digits
            result = cracker.brute_force_attack(args.min_length, args.max_length, charset, args.threads)
        elif args.patterns:
            result = cracker.pattern_attack(args.patterns, args.threads)
        else:
            print("[-] Please specify an attack method: -w (wordlist), -b (brute force), or -p (patterns)")
            sys.exit(1)
        
        if result:
            print(f"\n[+] Success! Password: {result}")
            
            # Show statistics
            stats = cracker.get_stats()
            if stats:
                print(f"[*] Attempts: {stats['attempts']:,}")
                print(f"[*] Time: {stats['elapsed_time']:.2f} seconds")
                print(f"[*] Rate: {stats['rate']:.1f} passwords/second")
        else:
            print("\n[-] Password not found")
            stats = cracker.get_stats()
            if stats:
                print(f"[*] Attempts: {stats['attempts']:,}")
                print(f"[*] Time: {stats['elapsed_time']:.2f} seconds")
    
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
