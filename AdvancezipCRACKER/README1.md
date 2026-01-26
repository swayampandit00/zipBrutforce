# AES ZIP Password Cracker - Advanced Method

## 🆕 आज का Method (AES ZIP Cracking)

आज हमने एक advanced ZIP password cracker बनाया जो **AES encryption** वाली ZIP files को crack कर सकता है।

### 🔥 Key Features

- **AES Support**: WinZIP AES encryption (compression method 99) को handle करता है
- **High Performance**: Multiprocessing के साथ fast cracking
- **Multiple Attacks**: Dictionary और brute force attacks
- **Real-time Progress**: Live statistics और progress tracking

## 📦 Installation

```bash
# Install required library for AES support
pip install pyzipper

# Verify installation
python -c "import pyzipper; print('AES support ready!')"
```

## 🚀 How to Use

### 1. Dictionary Attack (Recommended)

```bash
# Basic dictionary attack
python zip_cracker_aes.py your_file.zip -w wordlist.txt

# With multiple threads for faster performance
python zip_cracker_aes.py your_file.zip -w wordlist.txt -t 8

# Verbose mode for detailed output
python zip_cracker_aes.py your_file.zip -w wordlist.txt -v
```

### 2. Brute Force Attack

```bash
# Basic brute force (1-6 characters, lowercase+digits)
python zip_cracker_aes.py your_file.zip -b

# Custom character set and length
python zip_cracker_aes.py your_file.zip -b --min-length 4 --max-length 8 --charset "0123456789"

# Only numbers (perfect for numeric passwords)
python zip_cracker_aes.py your_file.zip -b --charset "0123456789" --min-length 4 --max-length 6
```

### 3. Advanced Options

```bash
# Use all threads for maximum speed
python zip_cracker_aes.py your_file.zip -w wordlist.txt -t 12

# Custom character set with symbols
python zip_cracker_aes.py your_file.zip -b --charset "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$"

# Verbose debugging
python zip_cracker_aes.py your_file.zip -w wordlist.txt -v -t 4
```

## 🎯 Real Example (आज का Success Case)

```bash
# Problem: test_zip.zip with AES encryption
python zip_cracker_aes.py test_zip.zip -w word.txt

# Output:
[*] Starting AES dictionary attack with word.txt
[*] Using 4 workers
[*] Loaded 11,100 passwords
[*] Tried 4,500/11,100 passwords (398.1 pwd/s)
[+] PASSWORD FOUND: 3456

[+] Success! Password: 3456
[*] Attempts: 4,585
[*] Time: 11.60 seconds
[*] Rate: 395.4 passwords/second
```

## ✅ Advantages of AES Method

### 1. **🔓 Universal Compatibility**
- **Standard ZIP**: Traditional ZIP encryption (method 0)
- **AES-128**: WinZIP AES 128-bit encryption
- **AES-256**: WinZIP AES 256-bit encryption
- **All Compression Methods**: Deflate, BZip2, LZMA, etc.

### 2. **⚡ Superior Performance**
- **Multiprocessing**: Multiple CPU cores use करता है
- **Optimized Algorithm**: Fast password testing
- **Memory Efficient**: Large wordlists handle करता है
- **Real-time Stats**: Live progress monitoring

### 3. **🛡️ Advanced Features**
- **Error Handling**: Better error messages और debugging
- **Encoding Support**: UTF-8 wordlists handle करता है
- **Flexible Configuration**: Custom character sets और lengths
- **Thread Control**: Adjustable thread count

### 4. **🔍 Smart Detection**
- **Auto-detect**: Automatically detects encryption type
- **Compression Info**: Shows file details और compression method
- **Encryption Status**: Identifies if files are encrypted

## ⚠️ Limitations

### 1. **🔧 Dependencies Required**
```bash
# Must install pyzipper library
pip install pyzipper

# Not available in standard Python installation
# Requires external package installation
```

### 2. **💻 System Requirements**
- **Python 3.6+**: Newer Python version required
- **Memory Usage**: More RAM for large wordlists
- **CPU Intensive**: High CPU usage during cracking
- **Disk Space**: Temporary files के लिए space needed

### 3. **🔐 Encryption Limitations**
- **Strong Passwords**: Complex passwords take very long time
- **AES-256**: Very slow for brute force attacks
- **Large Key Spaces**: Exponential time complexity
- **No GPU Support**: CPU-only processing (no CUDA/OpenCL)

### 4. **⏱️ Time Constraints**
```bash
# Brute force time estimates (4-core CPU):
# 4-digit numbers: ~1 second
# 6-digit numbers: ~2 minutes  
# 8-character alphanumeric: ~years
# AES-256 brute force: ~impossible
```

## 📊 Performance Comparison

| Method | Standard ZIP | AES-128 | AES-256 | Speed |
|--------|--------------|---------|---------|-------|
| Old zip_cracker.py | ✅ | ❌ | ❌ | Fast |
| zip_cracker_aes.py | ✅ | ✅ | ✅ | Medium |

## 🎯 When to Use Which Method

### Use **Standard Method** (`zip_cracker.py`) जब:
- Simple ZIP files हों
- No external dependencies install करने हों
- Fast performance needed हो
- Standard encryption हो

### Use **AES Method** (`zip_cracker_aes.py`) जब:
- WinZIP AES encryption हो
- Modern ZIP files हों
- "Compression method not supported" error आए
- Unknown encryption type हो

## 🔧 Troubleshooting

### Common Issues और Solutions:

#### 1. "That compression method is not supported"
```bash
# Solution: Use AES method
python zip_cracker_aes.py file.zip -w wordlist.txt
```

#### 2. "No module named 'pyzipper'"
```bash
# Solution: Install pyzipper
pip install pyzipper
```

#### 3. Slow Performance
```bash
# Solution: Increase threads
python zip_cracker_aes.py file.zip -w wordlist.txt -t 8
```

#### 4. Memory Issues
```bash
# Solution: Reduce threads, use smaller wordlist
python zip_cracker_aes.py file.zip -w wordlist.txt -t 2
```

## 📈 Best Practices

### 1. **Start with Dictionary Attack**
```bash
# Always try dictionary first (much faster)
python zip_cracker_aes.py file.zip -w common_passwords.txt
```

### 2. **Use Appropriate Wordlists**
```bash
# For numeric passwords
python zip_cracker_aes.py file.zip -w numbers_wordlist.txt

# For common passwords
python zip_cracker_aes.py file.zip -w rockyou.txt
```

### 3. **Optimize Thread Count**
```bash
# Use CPU core count for best performance
python zip_cracker_aes.py file.zip -w wordlist.txt -t 8
```

### 4. **Monitor Progress**
```bash
# Use verbose mode for debugging
python zip_cracker_aes.py file.zip -w wordlist.txt -v
```

## 🎓 Learning Points

### आज हम सीखे:
1. **AES Encryption Detection**: Compression method 99 पहचानना
2. **Library Integration**: pyzipper का उपयोग
3. **Performance Optimization**: Multiprocessing के साथ speed
4. **Error Debugging**: Better error messages और troubleshooting
5. **Real-world Application**: Actual ZIP file crack करना

### Key Takeaway:
> **Standard ZIP cracker fails when AES encryption is present. Always try AES method for modern ZIP files.**

## 🚀 Next Steps

1. **Download More Wordlists**: RockYou, SecLists
2. **Try Pattern Attacks**: Common password combinations
3. **GPU Acceleration**: Explore hashcat जैसे tools
4. **Advanced Techniques**: Mask attacks, rule-based attacks

---

**🎯 Remember**: Use these tools ethically and only on files you own or have permission to test!
