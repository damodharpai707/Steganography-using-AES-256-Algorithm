# 🛡️ Steganography using AES-256 Algorithm

This project implements a secure steganography technique by combining the **Least Significant Bit (LSB)** method with **AES-256 encryption**. It allows users to hide sensitive text or images within a cover image, ensuring both **confidentiality** and **invisibility**.

## 🔐 Features
- **Text Steganography**: Embed secret text into an image using LSB.
- **Image Steganography**: Hide one image within another.
- **AES-256 Encryption**: Ensure secure transmission of the embedded data.
- **Data Retrieval**: Extract hidden data with authentication.
- **Image Quality Maintenance**: High PSNR values ensure minimal distortion in the stego image.

## ⚙️ Methodology
1. **LSB Encoding**:
   - Converts the secret data and the cover image into binary.
   - Substitutes the LSBs of the cover image pixels with secret data bits.
2. **AES-256 Encryption**:
   - Encrypts the stego image for additional security.
3. **Data Extraction**:
   - Performs AES decryption and LSB decoding to retrieve hidden data.

## 📈 Results
- **Minimal Distortion**: The stego images show negligible visual differences compared to the original cover images, ensuring invisibility of hidden data.
- **High PSNR Values**: High Peak Signal-to-Noise Ratio (PSNR) confirms the quality of the stego image.
- **Low MSE Values**: Low Mean Squared Error (MSE) indicates minimal changes to the cover image pixels during data embedding.

## 🛠️ Commands
### 📝 Text Steganography
- **Encryption**: `python3 cryptosteganography.py save -i <cover_image> -m <secret_message> -o <stego_image>`
- **Decryption**: `python3 cryptosteganography.py retrieve -i <stego_image>`

### 🖼️ Image Steganography
- **Encryption**: `python3 cryptosteganography.py save -i <cover_image> -s <secret_image> -o <stego_image>`
- **Decryption**: `python3 cryptosteganography.py retrieve -i <stego_image> -o <output_image>`

### 📊 Quality Metrics and Histogram Analysis
- **Calculate PSNR and MSE**: `python3 quality_metrics.py -c <cover_image> -s <stego_image>`
- **Generate Histogram Analysis**: `python3 histogram_analysis.py -c <cover_image> -s <stego_image> -o <output_histogram_image>`

## 💳 Applications
- Military communication.
- Smart ID cards.
- Secure one-time password storage.
- Digital watermarking.

## 🚀 Future Work
- Expand to **audio** and **video steganography**.
- Experiment with advanced steganographic algorithms.

## 📖 How to Run
1. Clone the repository: `git clone https://github.com/damodharpai707/Steganography-using-AES-256-Algorithm.git`
2. Follow the instructions in the code to input your cover image and data or follow the project report at [Github](https://github.com/damodharpai707/Steganography-using-AES-256-Algorithm/blob/main/Project%20Report.pdf).
3. Use the provided commands for encryption and decryption.

