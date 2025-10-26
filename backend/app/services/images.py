from pathlib import Path
from PIL import Image
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'tiff', 'bmp', 'webp'}

def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_process_file(stream, dest: Path) -> tuple[Path, str]:
    """
    Save and process uploaded file for AI processing.
    Simplified version for AI-focused certificate verifier.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dest, 'wb') as f:
        f.write(stream.read())
    
    file_ext = dest.suffix.lower()
    
    try:
        if file_ext == '.pdf':
            # For this AI project, we'll treat PDFs as valid but process them as generic files
            logger.info(f"PDF file saved: {dest}")
            return dest, 'pdf'
        else:
            # Validate image files using Pillow
            img = Image.open(dest)
            img.verify()
            
            # Re-open after verify (verify closes the image)
            img = Image.open(dest)
            
            # Convert to RGB if necessary for consistency
            if img.mode not in ['RGB', 'L']:
                img = img.convert('RGB')
                # Save the converted image
                img.save(dest, 'PNG', optimize=True)
                logger.info(f"Image converted to RGB: {dest}")
            
            return dest, 'image'
            
    except Exception as e:
        dest.unlink(missing_ok=True)
        raise ValueError(f"Invalid file format or corrupted file: {str(e)}")
