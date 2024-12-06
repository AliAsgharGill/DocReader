import os
import json
import yaml
from openpyxl import load_workbook
from xml.etree import ElementTree
from docx import Document
from pptx import Presentation
from PIL import Image
import mimetypes

class UnifiedFileReader:
    @staticmethod
    def read_file(file_name):
        # Get full path of the file in the current directory
        file_path = os.path.join(os.getcwd(), file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_name}")

        # Detect file type
        file_type, _ = mimetypes.guess_type(file_path)
        
        if not file_type:
            raise ValueError(f"Unknown file type for {file_path}")

        # Route to the correct file reader
        if file_type == "application/json":
            return UnifiedFileReader.read_json(file_path)
        elif file_type in ["text/x-yaml", "application/x-yaml"]:
            return UnifiedFileReader.read_yaml(file_path)
        elif file_type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            return UnifiedFileReader.read_excel(file_path)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return UnifiedFileReader.read_word(file_path)
        elif file_type in ["application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
            return UnifiedFileReader.read_ppt(file_path)
        elif file_type == "application/xml":
            return UnifiedFileReader.read_xml(file_path)
        elif file_type in ["image/png", "image/jpeg"]:
            return UnifiedFileReader.read_image(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def read_json(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    @staticmethod
    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def read_excel(file_path):
        wb = load_workbook(file_path)
        sheet = wb.active
        return [[cell.value for cell in row] for row in sheet.rows]

    @staticmethod
    def read_word(file_path):
        doc = Document(file_path)
        return [para.text for para in doc.paragraphs]

    @staticmethod
    def read_ppt(file_path):
        ppt = Presentation(file_path)
        slides = []
        for slide in ppt.slides:
            slides.append([shape.text for shape in slide.shapes if shape.has_text_frame])
        return slides

    @staticmethod
    def read_xml(file_path):
        tree = ElementTree.parse(file_path)
        root = tree.getroot()
        return ElementTree.tostring(root, encoding="unicode")

    @staticmethod
    def read_image(file_path):
        with Image.open(file_path) as img:
            return {
                "format": img.format,
                "size": img.size,
                "mode": img.mode,
                "data": img.tobytes(),
            }

# Example Usage
if __name__ == "__main__":
    file_name = "one.py"
    reader = UnifiedFileReader()
    data = reader.read_file(file_name)
    print(data)
