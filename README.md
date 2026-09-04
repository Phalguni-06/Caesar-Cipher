# Caesar Cipher — Professional Edition

A Python command-line Caesar cipher toolkit for encryption, decryption, cryptanalysis, and learning.

## Features

- Encryption/decryption with configurable shift
- Brute-force decryption across all 26 shifts
- Letter frequency analysis
- Chi-squared English-likelihood test
- Common English word matching
- Combined scoring and confidence estimates
- Ciphertext statistics and frequency bars
- Educational mode
- Interactive terminal menu
- Importable Python functions
- Works in Jupyter and terminal

## Requirements

- Python 3.8+
- No third-party packages required

## Run

```bash
python caesar_cipher_pro.py
```

## Options

1. Encrypt text (with known shift)
2. Decrypt text (with known shift)
3. Brute-force decrypt (try all shifts)
4. Analyze ciphertext
5. Educational mode (guided analysis)
6. Exit

## Import

```python
from caesar_cipher_pro import encrypt, decrypt, brute_force_decrypt

ciphertext = encrypt("hello", 2)
print(ciphertext)  # jgnnq

plaintext = decrypt(ciphertext, 2)
print(plaintext)   # hello

results = brute_force_decrypt(ciphertext)
print(results)
```

## Example

```text
Plaintext:   hello
Shift Value: 2
Ciphertext:  jgnnq
```

## Security note

Caesar cipher is a classical educational cipher and is not suitable for protecting real secrets. There are only 26 possible shifts, making brute-force attacks straightforward. Use modern cryptographic algorithms for real security.

## Project structure

```text
caesar-cipher-professional/
├── caesar_cipher_pro.py
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
└── .github/
    └── workflows/
        └── python-check.yml
```

## GitHub upload

```bash
git init
git add .
git commit -m "Initial Caesar Cipher Professional Edition"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## License

MIT License
