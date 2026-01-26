# ZIP Password Cracker

A powerful Python tool for cracking ZIP file passwords using multiple attack methods including dictionary attacks, brute force attacks, and pattern-based attacks.

## Features

- **Dictionary Attack**: Use wordlists to test common passwords
- **Brute Force Attack**: Try all possible combinations within specified parameters
- **Pattern-Based Attack**: Generate passwords based on common patterns
- **Multiprocessing Support**: Utilize multiple CPU cores for faster cracking
- **Progress Tracking**: Real-time statistics and progress updates
- **Flexible Configuration**: Customizable character sets, password lengths, and patterns

## Installation

No external dependencies required! This tool uses only Python's standard library.

```bash
# Ensure you have Python 3.6+ installed
python --version

# Clone or download the script
git clone <repository-url>
cd zipbrut
```

## Usage

### Basic Syntax

```bash
python zip_cracker.py <zip_file> [options]
```

### Attack Methods

#### 1. Dictionary Attack

```bash
# Use a wordlist file
python zip_cracker.py protected.zip -w wordlist.txt

# With multiple threads
python zip_cracker.py protected.zip -w rockyou.txt -t 8
```

#### 2. Brute Force Attack

```bash
# Basic brute force (lowercase + digits, length 1-6)
python zip_cracker.py protected.zip -b

# Custom character set and length
python zip_cracker.py protected.zip -b --charset "abcdefghijklmnopqrstuvwxyz0123456789" --min-length 4 --max-length 8

# Using all printable characters
python zip_cracker.py protected.zip -b --charset "$(python -c 'import string; print(string.printable)')" --min-length 1 --max-length 4
```

#### 3. Pattern-Based Attack

```bash
# Use common password patterns
python zip_cracker.py protected.zip -p word+number word+symbol capitalized leet

# Multiple patterns with threads
python zip_cracker.py protected.zip -p word+number capitalized -t 4
```

### Options

- `-w, --wordlist`: Path to wordlist file
- `-b, --brute`: Use brute force attack
- `-p, --patterns`: Use pattern-based attack (choices: word+number, word+symbol, capitalized, leet)
- `--min-length`: Minimum password length for brute force (default: 1)
- `--max-length`: Maximum password length for brute force (default: 6)
- `--charset`: Character set for brute force (default: lowercase+digits)
- `-t, --threads`: Number of threads to use (default: CPU count)
- `-v, --verbose`: Verbose output

### Examples

```bash
# Quick dictionary attack with common passwords
python zip_cracker.py archive.zip -w common_passwords.txt

# Intensive brute force with custom settings
python zip_cracker.py archive.zip -b --min-length 6 --max-length 10 --charset "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$" -t 12

# Combined pattern attack
python zip_cracker.py archive.zip -p word+number capitalized leet -t 6

# Verbose mode for detailed output
python zip_cracker.py archive.zip -w wordlist.txt -v
```

## Wordlists

### Common Wordlist Sources

1. **RockYou**: Most popular password list
   - Download: `https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt`

2. **SecLists**: Comprehensive collection of wordlists
   - GitHub: `https://github.com/danielmiessler/SecLists`

3. **Create Custom Wordlist**:
```bash
# Generate from website content
curl https://example.com | grep -oE '\w{4,}' | sort -u > custom_wordlist.txt

# Combine multiple wordlists
cat wordlist1.txt wordlist2.txt | sort -u > combined_wordlist.txt
```

## Performance Tips

1. **Use Multiple Threads**: Leverage all CPU cores with `-t` option
2. **Start with Dictionary**: Dictionary attacks are much faster than brute force
3. **Smart Brute Force**: Start with shorter lengths and common character sets
4. **Pattern Attacks**: Often faster than pure brute force for predictable passwords

## Character Sets

Common character sets for brute force:

```bash
# Lowercase letters
--charset "abcdefghijklmnopqrstuvwxyz"

# Uppercase letters  
--charset "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Numbers
--charset "0123456789"

# Common symbols
--charset "!@#$%^&*"

# All alphanumeric
--charset "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# All printable characters (Python)
--charset "$(python -c 'import string; print(string.printable.rstrip())')"
```

## Pattern Types

- `word+number`: Common words followed by numbers (password123, admin2024)
- `word+symbol`: Words with symbols (password!, admin@)
- `capitalized`: Capitalized versions (Password, Admin)
- `leet`: Leet speak substitutions (P@ssw0rd, 4dm1n)

## Output Examples

### Successful Attack
```
[*] Starting dictionary attack with wordlist.txt
[*] Using 8 workers
[*] Loaded 14,344,391 passwords
[*] Tried 1,000/14,344,391 passwords (2,345.2 pwd/s)
[+] PASSWORD FOUND: secret123

[+] Success! Password: secret123
[*] Attempts: 45,678
[*] Time: 19.47 seconds
[*] Rate: 2,345.2 passwords/second
```

### Unsuccessful Attack
```
[*] Starting brute force attack
[*] Character set: abcdefghijklmnopqrstuvwxyz0123456789
[*] Password length: 1-6
[*] Using 8 workers
[*] Total combinations to try: 2,176,782,336
[-] Password not found in brute force range

[-] Password not found
[*] Attempts: 2,176,782,336
[*] Time: 928.34 seconds
```

## Security & Legal

**⚠️ IMPORTANT**: Only use this tool on ZIP files you own or have explicit permission to test. Unauthorized password cracking may be illegal in your jurisdiction.

- Use responsibly and ethically
- Respect privacy and property rights
- Follow applicable laws and regulations
- Educational purposes only

## Troubleshooting

### Common Issues

1. **"Invalid ZIP file format"**
   - Ensure the file is a valid ZIP archive
   - Check if the file is corrupted

2. **"ZIP file is empty"**
   - The ZIP file contains no files to extract
   - Try with a different ZIP file

3. **Slow Performance**
   - Increase thread count with `-t` option
   - Use a more targeted wordlist
   - Reduce brute force search space

4. **Memory Issues**
   - Use smaller wordlists
   - Reduce thread count
   - Break large wordlists into smaller chunks

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: Standard library only
- **Performance**: ~2M+ passwords/second (depends on hardware)
- **Threading**: ThreadPoolExecutor for parallel processing
- **ZIP Support**: Standard ZIP encryption (not AES)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

## License

This project is for educational purposes. Use responsibly and in accordance with applicable laws.
