"""Image Preprocessing Module - Extract entropy-rich noise from space images"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
import hashlib
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """Extracts high-entropy noise from images"""
    
    def __init__(self, block_size: int = 4096):
        """
        Initialize preprocessor
        
        Args:
            block_size: Target size for extracted entropy blocks (bytes)
        """
        self.block_size = block_size
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image as numpy array or None if failed
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            return image
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale
        
        Args:
            image: Input image (BGR or RGB)
            
        Returns:
            Grayscale image
        """
        if len(image.shape) == 2:
            # Already grayscale
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def extract_laplacian_noise(self, image: np.ndarray) -> np.ndarray:
        """
        Extract high-frequency noise using Laplacian filter
        
        Laplacian highlights edges and rapid intensity changes,
        which contain high entropy in natural images
        
        Args:
            image: Grayscale image
            
        Returns:
            Noise array
        """
        # Apply Laplacian filter to detect edges
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        
        # Take absolute values
        noise = np.abs(laplacian)
        
        # Add original image to preserve some structure
        # This prevents too many zeros
        combined = noise + image.astype(np.float64) * 0.3
        
        # Normalize to 0-255
        if combined.max() > combined.min():
            noise = ((combined - combined.min()) / (combined.max() - combined.min()) * 255).astype(np.uint8)
        else:
            noise = combined.astype(np.uint8)
        
        return noise
    
    def extract_fft_high_freq(self, image: np.ndarray, cutoff_ratio: float = 0.7) -> np.ndarray:
        """
        Extract high-frequency components using FFT
        
        High-frequency components contain noise and fine details
        
        Args:
            image: Grayscale image
            cutoff_ratio: Fraction of frequencies to keep (0-1)
            
        Returns:
            High-frequency component image
        """
        # Apply 2D FFT
        f_transform = np.fft.fft2(image)
        f_shift = np.fft.fftshift(f_transform)
        
        # Create high-pass filter (keep outer frequencies)
        rows, cols = image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Calculate radius for high-pass filter
        radius = int(min(crow, ccol) * (1 - cutoff_ratio))
        
        # Create mask (1 for high freq, 0 for low freq)
        mask = np.ones((rows, cols), dtype=np.uint8)
        y, x = np.ogrid[:rows, :cols]
        mask_area = (x - ccol)**2 + (y - crow)**2 <= radius**2
        mask[mask_area] = 0
        
        # Apply mask
        f_shift_filtered = f_shift * mask
        
        # Inverse FFT
        f_ishift = np.fft.ifftshift(f_shift_filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        
        # Normalize to 0-255
        if img_back.max() > 0:
            img_back = (img_back / img_back.max() * 255).astype(np.uint8)
        else:
            img_back = img_back.astype(np.uint8)
        
        return img_back
    
    def extract_pixel_differences(self, image: np.ndarray) -> np.ndarray:
        """
        Extract pixel-to-pixel differences (gradient)
        
        Differences between adjacent pixels contain high entropy
        
        Args:
            image: Grayscale image
            
        Returns:
            Difference array
        """
        # Calculate gradients in X and Y directions
        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Combine gradients
        gradient = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize to 0-255
        if gradient.max() > 0:
            gradient = (gradient / gradient.max() * 255).astype(np.uint8)
        else:
            gradient = gradient.astype(np.uint8)
        
        return gradient
    
    def sample_random_regions(self, image: np.ndarray, num_regions: int = 10, 
                             region_size: Tuple[int, int] = (64, 64)) -> List[np.ndarray]:
        """
        Sample random regions from image (non-deterministic)
        
        Uses current time and image hash for seeding to avoid deterministic patterns
        
        Args:
            image: Input image
            num_regions: Number of regions to sample
            region_size: Size of each region (height, width)
            
        Returns:
            List of image regions
        """
        if image.size == 0:
            return []
        
        height, width = image.shape[:2]
        reg_h, reg_w = region_size
        
        # Non-deterministic seed based on time and image content
        seed = abs(int(time.time() * 1000000) ^ hash(image.tobytes()[:1000]))
        rng = np.random.default_rng(seed)
        
        regions = []
        for _ in range(num_regions):
            # Random position
            if height > reg_h and width > reg_w:
                y = rng.integers(0, height - reg_h)
                x = rng.integers(0, width - reg_w)
                region = image[y:y+reg_h, x:x+reg_w]
                regions.append(region)
        
        return regions
    
    def separate_rgb_channels(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Separate RGB channels for individual processing
        
        Each channel contains unique noise characteristics
        
        Args:
            image: Color image (BGR format from OpenCV)
            
        Returns:
            List of [blue, green, red] channels
        """
        if len(image.shape) == 2:
            # Grayscale, return as single channel
            return [image]
        
        return [image[:, :, i] for i in range(image.shape[2])]
    
    def extract_noise(self, image_path: str) -> bytes:
        """
        Extract high-entropy noise from an image using multiple methods
        
        This is the main entry point that combines all extraction techniques
        
        Args:
            image_path: Path to image file
            
        Returns:
            Raw bytes with high entropy content
        """
        # Load image
        image = self.load_image(image_path)
        if image is None:
            logger.error(f"Cannot extract noise from {image_path}")
            return bytes()
        
        logger.info(f"Processing image: {Path(image_path).name}")
        
        collected_bytes = bytearray()
        
        # Method 1: Process each RGB channel separately
        channels = self.separate_rgb_channels(image)
        for i, channel in enumerate(channels):
            # Convert to grayscale if needed
            if len(channel.shape) > 2:
                channel = self.convert_to_grayscale(channel)
            
            # Extract Laplacian noise
            laplacian = self.extract_laplacian_noise(channel)
            collected_bytes.extend(laplacian.flatten().tobytes())
            
            logger.debug(f"  Channel {i}: Laplacian noise extracted ({len(laplacian.flatten())} bytes)")
        
        # Method 2: Full grayscale processing
        gray = self.convert_to_grayscale(image)
        
        # Extract FFT high-frequency components
        fft_noise = self.extract_fft_high_freq(gray, cutoff_ratio=0.8)
        collected_bytes.extend(fft_noise.flatten().tobytes())
        logger.debug(f"  FFT high-freq noise extracted ({len(fft_noise.flatten())} bytes)")
        
        # Extract pixel differences (gradients)
        diff_noise = self.extract_pixel_differences(gray)
        collected_bytes.extend(diff_noise.flatten().tobytes())
        logger.debug(f"  Gradient noise extracted ({len(diff_noise.flatten())} bytes)")
        
        # Method 3: Sample random regions
        regions = self.sample_random_regions(gray, num_regions=5, region_size=(32, 32))
        for region in regions:
            # Extract noise from each region
            region_noise = self.extract_laplacian_noise(region)
            collected_bytes.extend(region_noise.flatten().tobytes())
        
        logger.debug(f"  Random regions sampled ({len(regions)} regions)")
        
        # Don't use simple XOR mix - it reduces entropy
        # Instead, return the raw collected bytes
        logger.info(f"✓ Extracted {len(collected_bytes)} raw noise bytes from {Path(image_path).name}")
        
        return bytes(collected_bytes)
    
    def _xor_mix(self, data: bytearray) -> bytearray:
        """
        Mix bytes using XOR to distribute entropy
        
        Args:
            data: Input byte array
            
        Returns:
            Mixed byte array
        """
        if len(data) < 2:
            return data
        
        mixed = bytearray(len(data))
        
        # XOR each byte with the next byte (circular)
        for i in range(len(data)):
            mixed[i] = data[i] ^ data[(i + 1) % len(data)]
        
        return mixed
    
    def extract_noise_batch(self, image_paths: List[str]) -> bytes:
        """
        Extract noise from multiple images and combine
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Combined raw bytes from all images
        """
        all_noise = bytearray()
        
        for path in image_paths:
            noise = self.extract_noise(path)
            all_noise.extend(noise)
        
        logger.info(f"✓ Batch extracted {len(all_noise)} bytes from {len(image_paths)} images")
        
        return bytes(all_noise)


# Global preprocessor instance
preprocessor = ImagePreprocessor()


if __name__ == "__main__":
    # Test with downloaded NASA images
    import sys
    from app.ingestion import ingestion_manager
    
    print("Testing Image Preprocessor")
    print("=" * 60)
    
    # Get stored images
    images = ingestion_manager.get_stored_images()
    
    if not images:
        print("No images found. Run test_ingestion.py first.")
        sys.exit(1)
    
    print(f"Found {len(images)} images\n")
    
    # Test with first image
    test_image = images[0]
    print(f"Processing: {Path(test_image).name}")
    print("-" * 60)
    
    noise_data = preprocessor.extract_noise(test_image)
    
    print(f"\nExtracted {len(noise_data):,} noise bytes")
    print(f"First 32 bytes: {noise_data[:32].hex()}")
    
    # Quick entropy check
    from app.entropy.validation import validator
    result = validator.validate(noise_data[:4096], detailed=True)
    
    print("\nEntropy Validation:")
    print("-" * 60)
    for key, value in result.items():
        print(f"{key}: {value}")
