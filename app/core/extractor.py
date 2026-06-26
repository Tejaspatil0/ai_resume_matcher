import PyPDF2
import pdfplumber
import re


def extract_text_with_pypdf2(file_bytes):
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(file_bytes)

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"PyPDF2 error: {e}")
        return ""

    return text


def extract_text_with_pdfplumber(file_bytes):
    text = ""

    try:
        with pdfplumber.open(file_bytes) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(f"pdfplumber error: {e}")
        return ""

    return text


def extract_text_from_pdf(file_bytes):
    file_bytes.seek(0)
    text_pypdf2 = extract_text_with_pypdf2(file_bytes)

    if len(text_pypdf2.strip()) > 100:
        print("✅ Extracted with PyPDF2")
        return text_pypdf2

    print("⚠️ PyPDF2 gave poor results, trying pdfplumber...")

    file_bytes.seek(0)
    text_pdfplumber = extract_text_with_pdfplumber(file_bytes)

    if len(text_pdfplumber.strip()) > 100:
        print("✅ Extracted with pdfplumber")
        return text_pdfplumber

    print("⚠️ Both extractors gave limited results")
    return text_pypdf2 or text_pdfplumber


def extract_text_from_txt(file_bytes):
    try:
        file_bytes.seek(0)
        return file_bytes.read().decode("utf-8")

    except UnicodeDecodeError:
        file_bytes.seek(0)
        return file_bytes.read().decode("latin-1")


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def extract_text(uploaded_file_bytes, file_extension):
    try:
        if file_extension == "pdf":
            raw_text = extract_text_from_pdf(uploaded_file_bytes)

        elif file_extension == "txt":
            raw_text = extract_text_from_txt(uploaded_file_bytes)

        else:
            return {
                "success": False,
                "text": "",
                "word_count": 0,
                "char_count": 0,
                "error": f"Unsupported file type: {file_extension}"
            }

        cleaned_text = clean_text(raw_text)

        return {
            "success": True,
            "text": cleaned_text,
            "word_count": len(cleaned_text.split()),
            "char_count": len(cleaned_text),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "word_count": 0,
            "char_count": 0,
            "error": str(e)
        }