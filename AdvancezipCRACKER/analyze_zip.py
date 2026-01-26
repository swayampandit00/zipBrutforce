#!/usr/bin/env python3
"""
ZIP File Analysis Tool
"""

import zipfile
import os

def analyze_zip_file(zip_file):
    """Analyze ZIP file details"""
    print('=== ZIP FILE ANALYSIS ===')
    
    if not os.path.exists(zip_file):
        print(f'File {zip_file} not found')
        return
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            print(f'File: {zip_file}')
            print(f'Total files: {len(zf.namelist())}')
            
            for info in zf.infolist():
                print(f'\nFile: {info.filename}')
                print(f'  Size: {info.file_size} bytes')
                print(f'  Compressed: {info.compress_size} bytes')
                print(f'  Compression method: {info.compress_type}')
                print(f'  Flags: {info.flag_bits}')
                print(f'  Encrypted: {"Yes" if info.flag_bits & 0x1 else "No"}')
                
                # Check compression type
                if info.compress_type == 0:
                    comp_type = 'Store (no compression)'
                elif info.compress_type == 8:
                    comp_type = 'Deflate'
                elif info.compress_type == 12:
                    comp_type = 'BZip2'
                elif info.compress_type == 14:
                    comp_type = 'LZMA'
                elif info.compress_type == 99:
                    comp_type = 'AES WinZIP'
                else:
                    comp_type = f'Unknown ({info.compress_type})'
                
                print(f'  Compression type: {comp_type}')
                
                # Give recommendations
                print(f'\n  🎯 RECOMMENDATIONS:')
                if info.compress_type == 99:
                    print(f'    ✅ Use AES Method: python zip_cracker_aes.py {zip_file} -w wordlist.txt')
                    print(f'    ❌ Standard method will NOT work')
                elif info.flag_bits & 0x1:
                    print(f'    ✅ Use Standard Method: python zip_cracker.py {zip_file} -w wordlist.txt')
                    print(f'    ✅ AES Method will also work')
                else:
                    print(f'    ℹ️  File is NOT encrypted - no password needed!')
                
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    analyze_zip_file("test.zip")
