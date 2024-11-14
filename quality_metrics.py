"""-------------------------------------MSE and PSNR Analysis for Steganography: By Damodhar Pai------------------------------------------------"""
import numpy as np
from PIL import Image
import math
import argparse
import sys

def calculate_mse_psnr(cover_path, stego_path):
    """Calculate MSE and PSNR between cover and stego images."""
    try:
        # Load images
        cover_image = Image.open(cover_path).convert('RGB')
        stego_image = Image.open(stego_path).convert('RGB')
        
        # Convert to numpy arrays
        cover_array = np.array(cover_image)
        stego_array = np.array(stego_image)
        
        # Ensure images have same dimensions
        if cover_array.shape != stego_array.shape:
            raise ValueError("Images have different dimensions")
        
        # Calculate MSE for each channel
        mse_r = np.mean((cover_array[:,:,0] - stego_array[:,:,0]) ** 2)
        mse_g = np.mean((cover_array[:,:,1] - stego_array[:,:,1]) ** 2)
        mse_b = np.mean((cover_array[:,:,2] - stego_array[:,:,2]) ** 2)
        
        # Average MSE across channels
        mse = (mse_r + mse_g + mse_b) / 3
        
        # Calculate PSNR
        if mse == 0:
            psnr = float('inf')
        else:
            max_pixel = 255.0
            psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
        
        # Print results
        print("\nImage Quality Metrics:")
        print("-" * 50)
        print(f"Mean Square Error (MSE):")
        print(f"  Red Channel   : {mse_r:.6f}")
        print(f"  Green Channel : {mse_g:.6f}")
        print(f"  Blue Channel  : {mse_b:.6f}")
        print(f"  Average MSE   : {mse:.6f}")
        print(f"\nPeak Signal-to-Noise Ratio (PSNR):")
        print(f"  PSNR Value    : {psnr:.6f} dB")
        print("-" * 50)
        
        # Interpret results
        print("\nAnalysis:")
        if psnr >= 40:
            print("✓ Excellent quality (PSNR >= 40 dB)")
        elif psnr >= 30:
            print("✓ Good quality (PSNR >= 30 dB)")
        elif psnr >= 20:
            print("⚠ Fair quality (PSNR >= 20 dB)")
        else:
            print("✗ Poor quality (PSNR < 20 dB)")
            
        if mse < 2:
            print("✓ Very low distortion (MSE < 2)")
        elif mse < 10:
            print("✓ Acceptable distortion (MSE < 10)")
        elif mse < 25:
            print("⚠ Moderate distortion (MSE < 25)")
        else:
            print("✗ High distortion (MSE >= 25)")
            
        return mse, psnr
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Calculate MSE and PSNR for steganographic images")
    parser.add_argument("-c", "--cover", required=True, help="Path to cover image")
    parser.add_argument("-s", "--stego", required=True, help="Path to stego image")
    
    args = parser.parse_args()
    
    try:
        mse, psnr = calculate_mse_psnr(args.cover, args.stego)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
