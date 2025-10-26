from pathlib import Path
from PIL import Image
import logging
from io import BytesIO
import pytesseract

logger = logging.getLogger(__name__)

def _ocr_image(img: Image.Image) -> str:
    try:
        # Basic preprocessing: convert to grayscale
        if img.mode != 'L':
            img = img.convert('L')
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        logger.error(f"pytesseract OCR failed: {str(e)}")
        raise


def run_ocr(file_path: Path) -> str:
    """
    Extract text from uploaded files using Tesseract OCR.
    - For images: run OCR directly
    - For PDFs: try to extract embedded text; if none, render pages and OCR
    """
    try:
        ext = file_path.suffix.lower()

        if not file_path.exists():
            raise RuntimeError(f"File not found: {file_path}")

        if ext not in ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.webp']:
            raise RuntimeError(f"Unsupported file format: {ext}")

        if ext == '.pdf':
            # Try to extract text directly using PyMuPDF
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(str(file_path))
                text_parts = []
                for page in doc:
                    t = page.get_text().strip()
                    if t:
                        text_parts.append(t)
                text = "\n".join(text_parts)
                # Fallback to image rendering + OCR if no embedded text
                if not text.strip():
                    for page in doc:
                        pix = page.get_pixmap(dpi=300)
                        img = Image.open(BytesIO(pix.tobytes('png')))
                        text_parts.append(_ocr_image(img))
                    text = "\n".join(text_parts)
                if not text.strip():
                    raise RuntimeError("No text found in PDF")
                logger.info(f"Extracted {len(text)} characters from PDF for AI processing")
                return text
            except Exception as e:
                logger.warning(f"PDF text extraction failed, falling back to OCR: {str(e)}")
                # As a last resort, try to rasterize the first page using PIL
                raise
        else:
            # Image OCR path
            try:
                img = Image.open(file_path)
                width, height = img.size
                logger.info(f"Processing image {ext}: {width}x{height} pixels")
            except Exception as e:
                raise RuntimeError(f"Cannot read image file: {str(e)}")

            text = _ocr_image(img)
            if not text.strip():
                raise RuntimeError("No text detected in image")
            logger.info(f"Extracted {len(text)} characters from image for AI processing")
            return text

    except Exception as e:
        logger.error(f"Text extraction failed for {file_path}: {str(e)}")
        raise RuntimeError(f"Failed to extract text from file: {str(e)}")
