#!/usr/bin/env python3
"""
Debug script to check ZIP file and wordlist
"""

import zipfile
import os

def check_zip_file(zip_path):
    """Check ZIP file details"""
    print(f"[*] Checking ZIP file: {zip_path}")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            print(f"    Files in ZIP: {zf.namelist()}")
            print(f"    Total files: {len(zf.namelist())}")
            
            # Check if it's encrypted
            for info in zf.infolist():
                if info.flag_bits & 0x1:  # Check encryption flag
                    print(f"    File '{info.filename}' is ENCRYPTED")
                else:
                    print(f"    File '{info.filename}' is NOT encrypted")
                    
    except Exception as e:
        print(f"    Error: {e}")

def check_wordlist(wordlist_path):
    """Check wordlist details"""
    print(f"[*] Checking wordlist: {wordlist_path}")
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            print(f"    Total lines: {len(lines)}")
            
            # Show first 10 passwords
            print("    First 10 passwords:")
            for i, line in enumerate(lines[:10]):
                password = line.strip()
                print(f"        {i+1}: '{password}'")
            
            # Show last 10 passwords
            print("    Last 10 passwords:")
            for i, line in enumerate(lines[-10:], len(lines)-9):
                password = line.strip()
                print(f"        {i}: '{password}'")
                
            # Check for common passwords
            common_passwords = ['password', '123456', 'admin', '123', 'test']
            found_common = []
            for line in lines:
                password = line.strip()
                if password in common_passwords:
                    found_common.append(password)
            
            if found_common:
                print(f"    Common passwords found: {found_common}")
            else:
                print("    No common passwords found")
                
    except Exception as e:
        print(f"    Error: {e}")

def test_manual_passwords(zip_path):
    """Test some common passwords manually"""
    print(f"[*] Testing common passwords on {zip_path}")
    
    test_passwords = ['password', '123456', 'admin', '123', 'test', '00', '01', '02']
    
    for password in test_passwords:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                first_file = zf.namelist()[0]
                zf.extract(first_file, pwd=password.encode('utf-8'))
            print(f"    [+] SUCCESS: Password is '{password}'")
            return password
        except:
            print(f"    [-] Failed: '{password}'")
    
    print("    [-] No common passwords worked")
    return None

if __name__ == "__main__":
    check_zip_file("test_zip.zip")
    print()
    check_wordlist("word.txt")
    print()
    test_manual_passwords("test_zip.zip")
