import io

import fitz
import pytesseract
from PIL import Image


# ==================================================
# TESSERACT CONFIGURATION
# ==================================================

# Tesseract is installed at this location on your PC.
# We already verified this path using PowerShell.

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ==================================================
# 1. EXTRACT TEXT USING PYMUPDF
# ==================================================

def extract_with_pymupdf(file_bytes):
    """
    Extract text directly from a normal text-based PDF.
    """

    extracted_pages = []

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    try:

        for page in document:

            page_text = page.get_text(
                "text"
            )

            if page_text and page_text.strip():

                extracted_pages.append(
                    page_text.strip()
                )

    finally:

        document.close()

    return "\n\n".join(
        extracted_pages
    ).strip()


# ==================================================
# 2. EXTRACT TEXT USING OCR
# ==================================================

def extract_with_ocr(file_bytes):
    """
    Extract text using Tesseract OCR.

    Used for scanned PDFs or PDFs that do not
    contain an extractable text layer.
    """

    extracted_pages = []

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    try:

        total_pages = len(document)

        print(
            f"OCR processing {total_pages} page(s)..."
        )

        for page_number, page in enumerate(
            document,
            start=1
        ):

            print(
                f"OCR processing page "
                f"{page_number}/{total_pages}..."
            )

            # Convert the PDF page into an image.
            # Matrix(2, 2) gives better OCR quality.
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            image_bytes = pix.tobytes(
                "png"
            )

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            # OCR text extraction
            page_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            if page_text and page_text.strip():

                extracted_pages.append(
                    page_text.strip()
                )

    finally:

        document.close()

    return "\n\n".join(
        extracted_pages
    ).strip()


# ==================================================
# 3. MAIN PDF EXTRACTION FUNCTION
# ==================================================

def extract_text_from_file(uploaded_file):
    """
    Extract text from an uploaded PDF.

    Process:

    1. Try direct PyMuPDF text extraction.
    2. If no text is found, use Tesseract OCR.
    """

    try:

        # ==========================================
        # READ UPLOADED FILE
        # ==========================================

        file_bytes = uploaded_file.getvalue()

        if not file_bytes:

            raise ValueError(
                "The uploaded file is empty."
            )


        # ==========================================
        # FILE INFORMATION
        # ==========================================

        file_size_kb = (
            len(file_bytes) / 1024
        )

        file_size_mb = (
            len(file_bytes) / (1024 * 1024)
        )

        print(
            "\n========== PDF EXTRACTION =========="
        )

        print(
            f"File name: {uploaded_file.name}"
        )

        if file_size_mb >= 1:

            print(
                f"File size: "
                f"{file_size_mb:.2f} MB"
            )

        else:

            print(
                f"File size: "
                f"{file_size_kb:.2f} KB"
            )


        # ==========================================
        # METHOD 1: DIRECT TEXT EXTRACTION
        # ==========================================

        print(
            "\nTrying PyMuPDF text extraction..."
        )

        text = extract_with_pymupdf(
            file_bytes
        )

        print(
            f"PyMuPDF extracted "
            f"{len(text)} characters."
        )


        # ==========================================
        # RETURN IF TEXT WAS FOUND
        # ==========================================

        if text and text.strip():

            print(
                "PyMuPDF extraction successful."
            )

            print(
                "====================================\n"
            )

            return text.strip()


        # ==========================================
        # METHOD 2: OCR FALLBACK
        # ==========================================

        print(
            "\nNo readable text found."
        )

        print(
            "Starting Tesseract OCR..."
        )

        text = extract_with_ocr(
            file_bytes
        )

        print(
            f"OCR extracted "
            f"{len(text)} characters."
        )


        # ==========================================
        # FINAL CHECK
        # ==========================================

        if not text or not text.strip():

            raise ValueError(
                "No text could be extracted "
                "using PyMuPDF or Tesseract OCR."
            )


        print(
            "OCR extraction successful."
        )

        print(
            "====================================\n"
        )

        return text.strip()


    except Exception as e:

        print(
            "\nPDF EXTRACTION ERROR:"
        )

        print(
            str(e)
        )

        print(
            "====================================\n"
        )

        raise ValueError(
            f"Could not extract text from PDF: {str(e)}"
        )