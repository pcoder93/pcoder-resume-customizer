from pathlib import Path
from typing import Optional
import yaml
from pylatex import Document, Command, NoEscape
from pylatex.utils import escape_latex
import os


class ModernCV:
    def __init__(self, path_profile, path_output=None):
        self.candidate_data = None
        self.path_output = None
        self.doc = None
        self._load_yaml(path_profile)
        self._set_path_output(path_output)

    def _load_yaml(self, path_profile):
        with open(path_profile, "r") as file:
            self.candidate_data = yaml.safe_load(file)
        print(self.candidate_data.keys())

    def _set_path_output(self, path_output: Optional[str | Path]):
        path_output = None
        if self.candidate_data:
            profile = self.candidate_data["profile"]
            if path_output is None:
                path_output = Path("local_data/" + "_".join([profile["name"], profile["label"]]) + "/")
                if not path_output.exists():
                    path_output.mkdir(parents=True)
            self.path_output = path_output
        print(self.path_output)

    # Function to add personal information
    def add_personal_info(self, profile):
        self.doc.preamble.append(Command("name", [profile["name"].split()[0], profile["name"].split()[1]]))
        self.doc.preamble.append(Command("title", profile.get("label", "")))
        self.doc.preamble.append(Command("email", profile.get("email", "")))
        self.doc.preamble.append(Command("phone", NoEscape(profile.get("phone", "")), r"mobile"))
        self.doc.preamble.append(Command("address", profile.get("address", "")))

    # Function to add a section with bullet points
    def add_section(self, title: str, items: list):
        self.doc.append(NoEscape(r"\section{" + escape_latex(title) + "}"))
        for item in items:
            self.doc.append(
                NoEscape(r"\cvitem{" + escape_latex(item["area"]) + r"}{" + ", ".join(item["skills"]) + r"}")
            )

    # Function to add work experience
    def add_work_experience(self, work):
        self.doc.append(NoEscape(r"\section{Professional Experience}"))
        for job in work:
            highlights = "\n\t".join(
                f"\\item {escape_latex(str(highlight).strip())}" for highlight in job["highlights"]
            )
            self.doc.append(
                NoEscape(
                    r"\cventry{"
                    + str(job.get("date", " "))
                    + "}{"
                    + escape_latex(job.get("role", " "))
                    + "}{"
                    + escape_latex(job.get("company", " "))
                    + "}{"
                    + escape_latex(job.get("website", " "))
                    + "}{}{"
                    + "\n"
                    + escape_latex(job.get("summary", " "))
                    + "\\begin{itemize}\n\t"
                    + highlights
                    + "\n"
                    + "\\end{itemize}\n}"
                )
            )

    # Function to add education
    def add_education(self, education):
        self.doc.append(NoEscape(r"\section{Education}"))
        for edu in education:
            self.doc.append(
                NoEscape(
                    r"\cventry{"
                    + edu.get("date", "")
                    + "}{"
                    + escape_latex(edu.get("summary", ""))
                    + "}{"
                    + escape_latex(edu.get("location", ""))
                    + "}{}{}{}"
                )
            )

    # Function to add projects
    def add_projects(self, projects):
        self.doc.append(NoEscape(r"\section{Projects}"))
        for project in projects:
            highlights = "\n\t".join(
                f"\\item {escape_latex(str(highlight).strip())}" for highlight in project["highlights"]
            )
            self.doc.append(
                NoEscape(
                    r"\cventry{"
                    + str(project.get("date", ""))
                    + "}{"
                    + escape_latex(project.get("name", ""))
                    + "}{"
                    + escape_latex(project.get("role", ""))
                    + "}{}{}{"
                    + escape_latex(project.get("website", ""))
                    + "\\begin{itemize}\n\t"
                    + highlights
                    + "\n"
                    + "\\end{itemize}\n}"
                )
            )

    # Function to add interests
    def add_interests(self, interests):
        self.doc.append(NoEscape(r"\section{Interests}"))
        self.doc.append(
            NoEscape(
                r"\cvitem{}{\begin{itemize}"
                + "\n"
                + "".join(f"\t\\item {escape_latex(interest)}\n" for interest in interests)
                + r"\end{itemize}}"
            )
        )

        # Main function to generate the CV

    def generate_cv(self):
        self.doc = Document(
            default_filepath=self.path_output.as_posix(),
            documentclass="moderncv",
            document_options="11pt,a4paper,roman",
        )
        self.doc.preamble.append(Command("moderncvstyle", "classic"))
        self.doc.preamble.append(Command("moderncvcolor", "blue"))
        self.doc.preamble.append(Command("usepackage", "ragged2e"))
        self.doc.preamble.append(Command("usepackage", arguments=["geometry"], options=["scale=0.75"]))
        self.doc.preamble.append(Command("usepackage", "fancyhdr"))
        self.doc.preamble.append(Command("setlength", arguments=[NoEscape(r"\hintscolumnwidth"), "3cm"]))
        self.doc.preamble.append(
            Command(
                "renewcommand*", arguments=[NoEscape(r"\namefont"), NoEscape(r"\fontsize{26}{28}\mdseries\upshape")]
            )
        )
        self.doc.preamble.append(
            Command("renewcommand*", arguments=[NoEscape(r"\labelitemi"), NoEscape(r"\textbullet")])
        )
        self.doc.append(NoEscape(r"\makecvtitle"))

        if isinstance(self.candidate_data, dict):
            if "profile" in self.candidate_data:
                self.add_personal_info(self.candidate_data["profile"])
            if "skills" in self.candidate_data:
                self.add_section("Skills", self.candidate_data["skills"])
            if "work" in self.candidate_data:
                self.add_work_experience(self.candidate_data["work"])
            if "projects" in self.candidate_data:
                self.add_projects(self.candidate_data["projects"])
            if "education" in self.candidate_data:
                self.add_education(self.candidate_data["education"])
            if "interests" in self.candidate_data:
                self.add_interests(self.candidate_data["interests"])
        self.doc.generate_pdf(self.path_output.as_posix() + "/resume", clean_tex=False)


# # Example usage
# generate_cv("resume.yml", "resume_output")
