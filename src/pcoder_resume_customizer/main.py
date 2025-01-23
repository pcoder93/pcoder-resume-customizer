from pcoder_resume_customizer.utils.config import settings
from pcoder_resume_customizer.tools.cli import cli

from pcoder_resume_customizer.moderncv import ModernCV

# def main():
#     from pylatex import Document, Command, Section
#     from pylatex.utils import NoEscape

# # Create the document with moderncv class
# doc = Document(documentclass="moderncv", document_options="11pt,a4paper,sans")

# # Add moderncv style and color
# doc.preamble.append(Command("moderncvstyle", "classic"))  # Style options: casual, classic, banking, oldstyle, fancy
# doc.preamble.append(Command("moderncvcolor", "blue"))  # Color options: black, blue, burgundy, etc.

# # Adjust page layout and fonts
# doc.preamble.append(NoEscape(r"\usepackage[scale=0.75]{geometry}"))
# doc.preamble.append(NoEscape(r"\setlength{\hintscolumnwidth}{3cm}"))
# doc.preamble.append(NoEscape(r"\renewcommand*{\namefont}{\fontsize{26}{28}\mdseries\upshape}"))

# # Personal data
# doc.preamble.append(Command("name", ["John", "Doe"]))
# doc.preamble.append(Command("title", "Curriculum Vitae"))
# doc.preamble.append(Command("address", ["123 Street Name", "City, Country"]))
# doc.preamble.append(Command("phone", [NoEscape(r"mobile"), "+1~(234)~567~890"]))
# doc.preamble.append(Command("email", "john.doe@example.com"))

# # Add input files (e.g., cvraw and personal_info)
# doc.append(NoEscape(r"\input{personal_info}"))
# doc.append(NoEscape(r"\input{cvraw}"))

# # Add clear page (optional for multi-page documents)
# doc.append(NoEscape(r"\clearpage"))

# # Generate the PDF
# doc.generate_pdf("local_data/test1", clean_tex=False)


if __name__ == "__main__":
    new_cv = ModernCV("/home/pranav/projects/pcoder-resume-customizer/pranav.yaml")
    new_cv.generate_cv()
