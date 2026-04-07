# Zyxel WAX650S $4$ Encrypted Password Decrypter

This repository contains a Python script to decrypt passwords encrypted with the Zyxel proprietary `$4$` scheme, commonly found in the `mfg-default.conf` configuration files of Zyxel WAX650S devices and potentially other Zyxel products.

## Background

The `$4$` scheme is used by Zyxel to store sensitive information, such as administrative passwords, in a reversible encrypted format rather than a one-way hash. Analysis of Zyxel firmware has revealed that this scheme utilizes **AES-192-CBC** encryption with a static key and Initialization Vector (IV) embedded within the `zysh` binary.

This tool was developed based on research by HN Security [1], which detailed the firmware extraction and password analysis process for Zyxel devices.

## Technical Details

The encryption process involves:
1.  **Salt**: An 8-byte ASCII salt is extracted from the `$4$` string.
2.  **Plaintext Preparation**: The plaintext password is combined with the salt and then padded or repeated to fill an 80-byte buffer.
3.  **Encryption**: AES-192-CBC is applied to the prepared plaintext using a static key and IV.
4.  **Encoding**: The resulting ciphertext is Base64 encoded.

### Identified AES Parameters

| Parameter | Value |
| :-------- | :---- |
| **Algorithm** | AES-192-CBC |
| **Key (Hex)** | `001200054A1F23FB1F060A14CD0D018F5AC0001306F0121C` |
| **IV (Hex)** | `0006001C01F01FC0FFFFFFFFFFFFFFFF` |

## Usage

### Prerequisites

- Python 3.x
- `pycryptodome` library: `pip install pycryptodome`

### Decryption

To decrypt a password, you need the full `$4$` string, which includes the salt and the Base64-encoded ciphertext. For example:

`$4$WliGKvFQ$yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U$`

From this string, extract the salt (`WliGKvFQ`) and the Base64-encoded value (`yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U`).

Then, run the `zyxel_decrypt.py` script, providing the salt and the Base64-encoded value:

```bash
python3 zyxel_decrypt.py "WliGKvFQ" "yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U"
```

The script will output the decrypted password.

## Example

Given the input:

`username admin encrypted-password $4$WliGKvFQ$yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U$ user-type admin`

Running the script with `salt = "WliGKvFQ"` and `value_b64 = "yMEH/WCnH1+NXuIUp0lzpUinIyEnrHFoRgesi6NdOFytmQg8lRgesi6NdOFytmQg8lRfsVzUUjBGY+FiS4Up6KIgoP8OMEP0L3hRYSN2kpFTDIet31GoNwlM+S7U"` will yield:

```
Salt: WliGKvFQ
Decrypted (raw): b'WliGKvFQ1234\x00123412341234123412341234123412341234123412341234123412341234123'
Decrypted Password: 1234
```

## Disclaimer

This tool is provided for educational and research purposes only. Use it responsibly and in accordance with applicable laws and regulations. The author is not responsible for any misuse or damage caused by this tool.

## References

[1] HN Security. *Zyxel firmware extraction and password analysis*. [https://hnsecurity.it/blog/zyxel-firmware-extraction-and-password-analysis/](https://hnsecurity.it/blog/zyxel-firmware-extraction-and-password-analysis/)
