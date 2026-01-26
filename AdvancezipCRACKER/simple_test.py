#!/usr/bin/env python3
"""
Simple test to check ZIP file and find password
"""

import zipfile

def test_password_simple(zip_path, password):
    """Simple password test"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Try to test without extracting
            for info in zf.infolist():
                print(f"File: {info.filename}")
                print(f"Compressed size: {info.compress_size}")
                print(f"Uncompressed size: {info.file_size}")
                print(f"Compression method: {info.compress_type}")
                print(f"Flags: {info.flag_bits}")
                print(f"Encrypted: {'Yes' if info.flag_bits & 0x1 else 'No'}")
                
                if info.flag_bits & 0x1:  # If encrypted
                    try:
                        # Try to read file data
                        with zf.open(info.filename, pwd=password.encode('utf-8')) as f:
                            data = f.read(10)  # Read first 10 bytes
                        print(f"[+] SUCCESS with password: '{password}'")
                        print(f"First 10 bytes: {data}")
                        return True
                    except Exception as e:
                        print(f"[-] Failed with password '{password}': {e}")
                else:
                    print("[+] File is not encrypted!")
                    return True
                    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return False

# Test with some passwords from your wordlist
zip_file = "test_zip.zip"
test_passwords = ["", "00", "01", "123", "1234", "000", "9999", "password"]

print(f"[*] Testing ZIP file: {zip_file}")
print("=" * 50)

for pwd in test_passwords:
    print(f"\n[*] Testing password: '{pwd}'")
    if test_password_simple(zip_file, pwd):
        print(f"[+] FOUND PASSWORD: '{pwd}'")
        break
    print("-" * 30)
