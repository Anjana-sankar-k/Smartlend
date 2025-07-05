import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_image(image):
    return pytesseract.image_to_string(image)

def parse_text_for_fields(text):
    print("\n------ OCR RAW TEXT ------\n", text)

    lines = text.splitlines()
    extracted = {
        "Name": None,
        "DOB": None,
        "Gender": None,
        "Aadhaar Number": None,
        "Monthly Income": None,
        "Email": None,
        "Phone": None
    }

    for line in lines:
        line = line.strip()

        # Employee Name
        if "employee name" in line.lower():
            name_match = re.search(r"Employee Name[:\-]?\s*(.+)", line, re.IGNORECASE)
            if name_match:
                extracted["Name"] = name_match.group(1).strip().title()

        # DOB
        if "dob" in line.lower() or "date of birth" in line.lower():
            dob_match = re.search(r"(DOB|Date of Birth)[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})", line, re.IGNORECASE)
            if dob_match:
                extracted["DOB"] = dob_match.group(2)

        # Gender
        if re.search(r"\b(male|female|transgender)\b", line, re.IGNORECASE):
            extracted["Gender"] = re.search(r"\b(male|female|transgender)\b", line, re.IGNORECASE).group(1).capitalize()

        # Aadhaar Number
        aadhaar_match = re.search(r"\b\d{4} \d{4} \d{4}\b", line)
        if aadhaar_match:
            extracted["Aadhaar Number"] = aadhaar_match.group(0)

        # Net salary
        if "net payable" in line.lower():
            net_pay_match = re.search(r"Net Payable Amount\s*[:\-]?\s*₹?\s*([\d,]+\.\d{2})", line, re.IGNORECASE)
            if net_pay_match:
                extracted["Monthly Income"] = net_pay_match.group(1).replace(",", "")

        # Email
        if "@" in line:
            email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            if email_match:
                extracted["Email"] = email_match.group(0)

        # Phone
        phone_match = re.search(r"\b[6-9]\d{9}\b", line)
        if phone_match:
            extracted["Phone"] = phone_match.group(0)

    return extracted


def parse_uploaded_documents(uploaded_files):
    # Start with an empty unified profile
    merged_fields = {
        "Name": None,
        "DOB": None,
        "Gender": None,
        "Aadhaar Number": None,
        "Monthly Income": None,
        "Email": None,
        "Phone": None
    }

    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()
        text = ""

        if uploaded_file.name.endswith(".pdf"):
            images = convert_from_bytes(file_bytes, poppler_path=r'C:\Release-24.08.0-0\poppler-24.08.0\Library\bin')
            for image in images:
                text += ocr_image(image) + "\n"
        else:
            image = Image.open(uploaded_file)
            text = ocr_image(image)

        parsed_fields = parse_text_for_fields(text)

        # Merge values if not already filled
        for key, value in parsed_fields.items():
            if value and not merged_fields[key]:
                merged_fields[key] = value

    return merged_fields
