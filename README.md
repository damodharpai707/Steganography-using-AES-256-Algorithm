# 🛡️ Steganography using AES-256 Algorithm

This project implements a secure steganography technique by combining the **Least Significant Bit (LSB)** method with **AES-256 encryption**. It allows users to hide sensitive text or images within a cover image, ensuring both **confidentiality** and **invisibility**.

## 🔐 Features
-  **Text Steganography**: Embed secret text into an image using LSB.
-  **Image Steganography**: Hide one image within another.
-  **AES-256 Encryption**: Ensure secure transmission of the embedded data.
-  **Data Retrieval**: Extract hidden data with authentication.
-  **Image Quality Maintenance**: High PSNR values ensure minimal distortion in the stego image.

## ⚙️ Methodology
1. **LSB Encoding**:
   -  Converts the secret data and the cover image into binary.
   -  Substitutes the LSBs of the cover image pixels with secret data bits.
2. **AES-256 Encryption**:
   -  Encrypts the stego image for additional security.
3. **Data Extraction**:
   -  Performs AES decryption and LSB decoding to retrieve hidden data.

## 📈 Results
- **PSNR and MSE**:
  -  Text steganography: **PSNR** = 50.11 dB, **MSE** = 0.63.
  -  Image steganography: **PSNR** = 56.78 dB, **MSE** = 0.14.
-  Minimal perceptible difference between cover and stego images.

## 🛠️ Commands
### 📝 Text Steganography
- **Encryption**: `python3 cryptosteganography.py save -i <cover_image> -m <secret_message> -o <stego_image>`
- **Decryption**: `python3 cryptosteganography.py retrieve -i <stego_image>`

### 🖼️ Image Steganography
- **Encryption**: `python3 cryptosteganography.py save -i <cover_image> -f <secret_image> -o <stego_image>`
- **Decryption**: `python3 cryptosteganography.py retrieve -i <stego_image>`

## 💳 Applications
-  Military communication.
-  Smart ID cards.
-  Secure one-time password storage.
-  Digital watermarking.

## 🚀 Future Work
-  Expand to **audio** and **video steganography**.
-  Experiment with advanced steganographic algorithms.

## 📖 How to Run
1. Clone the repository: `git clone https://github.com/damodharpai707/Steganography-using-AES-256-Algorithm.git`
2. Follow the instructions in the code to input your cover image and data.
3. Use the provided commands for encryption and decryption.
