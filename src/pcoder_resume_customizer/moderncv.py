from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml
from pylatex import Command, Document, NoEscape
from pylatex.utils import escape_latex

from pcoder_resume_customizer.utils.logging import logger


class ModernCV:
    def __init__(self, path_profile, path_job=None, save_path=None):
        self.save_path = None
        self.doc = None
        self.output_type = None
        self.candidate_data = self._load_yaml(path_profile)
        self.job_data = self._load_yaml(path_job) if path_job else None
        self._set_save_path(save_path)

    def _load_yaml(self, path_yaml_file):
        if Path(path_yaml_file).exists():
            data = {}
            with open(path_yaml_file, "r") as file:
                data = yaml.safe_load(file)
            logger.debug("Loaded data from %s: %s", path_yaml_file, data.keys())
            return data
        else:
            raise FileNotFoundError(f"File {path_yaml_file} not found")

    def _set_save_path(self, path: Optional[str | Path]):
        if path is None:
            if self.job_data:
                folder_name = "--".join(
                    [
                        datetime.now().strftime("%Y-%m-%d"),
                        (self.job_data["job"]["company_name"]).replace(" ", "_"),
                        (self.job_data["job"]["title"]).replace(" ", "_"),
                    ],
                )
            else:
                folder_name = "--".join(
                    [
                        datetime.now().strftime("%Y-%m-%d"),
                        "Job",
                    ]
                )
            ls_existing_folders = list(Path("Applications/").glob(f"{folder_name}*"))
            if len(ls_existing_folders) > 0:
                for folder in ls_existing_folders:
                    if folder.name == folder_name:
                        folder_name = folder_name + "_" + str(len(ls_existing_folders) + 1)

            path = Path("Applications/" + folder_name + "/")
            if not path.exists():
                path.mkdir(parents=True)
        else:
            path = Path(path)
        self.save_path = path
        logger.info("Save path: %s", self.save_path)
        if self.candidate_data:
            yaml.dump(self.candidate_data, open(self.save_path / "profile.yml", "w"))
        if self.job_data:
            yaml.dump(self.job_data, open(self.save_path / "job_details.yml", "w"))

    def add_personal_info(self, profile):
        self.doc.preamble.append(Command("name", [profile["name"].split()[0], profile["name"].split()[1]]))
        self.doc.preamble.append(Command("title", profile.get("label", "")))
        self.doc.preamble.append(Command("email", profile.get("email", "")))
        self.doc.preamble.append(Command("phone", NoEscape(profile.get("phone", "")), r"mobile"))
        self.doc.preamble.append(Command("address", profile.get("address", "")))
        if profile.get("photo"):
            file_path = Path(profile.get("photo"))
            if file_path.exists():
                self.doc.preamble.append(
                    NoEscape(
                        r"\photo"
                        + f"[{str(90)}pt]"
                        + f"[{str(0.4)}pt]"
                        + "{"
                        + f"{file_path.absolute().as_posix()}"
                        + "}"
                    )
                )
        ls_valid_social_types = [
            "arxiv",
            "battlenet",
            "bitbucket",
            "codeberg",
            "discord",
            "github",
            "gitlab",
            "googlescholar",
            "inspire",
            "instagram",
            "linkedin",
            "mastodon",
            "matrix",
            "orcid",
            "playstation",
            "researcherid",
            "researchgate",
            "signal",
            "skype",
            "soundcloud",
            "stackoverflow",
            "steam",
            "telegram",
            "tiktok",
            "twitch",
            "twitter",
            "whatsapp",
            "xbox",
            "xing",
        ]
        if len(profile.get("socials", [])) > 0:
            for social in profile.get("socials"):
                social_type = str(social["provider"]).lower()
                if social_type in ls_valid_social_types:
                    self.doc.preamble.append(
                        Command("social", options=[social_type], arguments=[social.get("username")])
                    )

    # Function to add a section with bullet points
    def add_section(self, title: str, items: list):
        self.doc.append(NoEscape(r"\section{" + escape_latex(title) + "}"))
        for item in items:
            self.doc.append(
                NoEscape(r"\cvitem{" + escape_latex(item["area"]) + r"}{" + ", ".join(item["skills"]) + r"}")
            )

    def add_awards(self, awards: list):
        self.doc.append(NoEscape(r"\section{" + escape_latex("Participations & Awards") + "}"))
        for award in awards:
            self.doc.append(
                NoEscape(r"\cvitem{" + escape_latex(award["year"]) + r"}{" + escape_latex(award["name"]) + r"}")
            )

    # Function to add work experience
    def add_work_experience(self, work):
        self.doc.append(NoEscape(r"\section{Professional Experience}"))
        for job in work:
            highlights = ""
            if job["highlights"]:
                highlights = "\n\t".join(
                    f"\\item {escape_latex(str(highlight).strip())}" for highlight in job["highlights"]
                )
                highlights = "\n" + "\\begin{itemize}\n\t" + highlights + "\n" + "\\end{itemize}\n"
            summary = ""
            if job["summary"]:
                summary = "\n" + escape_latex(job.get("summary", " "))
            self.doc.append(
                NoEscape(
                    r"\cventry{"
                    + str(job.get("date", " "))
                    + "}{"
                    + escape_latex(job.get("role", " "))
                    + "}{"
                    + escape_latex(job.get("company", " "))
                    + "}{"
                    + escape_latex(job.get("location", " "))
                    + "}{}{"
                    + summary
                    + highlights
                    + "}"
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
            if project["highlights"]:
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

    def add_languages(self, languages):
        self.doc.append(NoEscape(r"\section{Languages}"))
        ls_languages = self.candidate_data["languages"]
        for idx in range(0, len(ls_languages), 2):
            language_set = ls_languages[idx : idx + 2]
            if len(language_set) < 2:
                language_set.append({"language": "", "level": ""})
            self.doc.append(
                NoEscape(
                    r"\cvdoubleitem{"
                    + NoEscape(language_set[0]["language"])
                    + r"}{"
                    + NoEscape(language_set[0]["level"])
                    + r"}{"
                    + NoEscape(language_set[1]["language"])
                    + r"}{"
                    + NoEscape(language_set[1]["level"])
                    + r"}"
                )
            )

    def add_preamble(self):
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
        if "profile" in self.candidate_data:
            self.add_personal_info(self.candidate_data["profile"])
        else:
            raise ValueError(f"Profile data not found in the yaml file {self.path_profile}")

    def start_document(self):
        self.doc = Document(
            default_filepath=self.save_path.as_posix(),
            documentclass="moderncv",
            document_options="11pt,a4paper,sans",
        )
        self.add_preamble()

    def generate_cv(self):
        if self.doc is None:
            self.output_type = "CV"
            self.start_document()

        self.doc.append(NoEscape(r"\makecvtitle"))

        if isinstance(self.candidate_data, dict):
            if "work" in self.candidate_data:
                self.add_work_experience(self.candidate_data["work"])
            if "education" in self.candidate_data:
                self.add_education(self.candidate_data["education"])
            if "skills" in self.candidate_data:
                self.add_section("Skills", self.candidate_data["skills"])
            if "projects" in self.candidate_data:
                self.add_projects(self.candidate_data["projects"])
            if "awards" in self.candidate_data:
                self.add_awards(self.candidate_data["awards"])
            if "interests" in self.candidate_data:
                self.add_interests(self.candidate_data["interests"])
            if "languages" in self.candidate_data:
                self.add_languages(self.candidate_data["languages"])

    def generate_cover_letter(self):
        if self.doc is None:
            self.output_type = "CL"
            self.start_document()
        else:
            self.doc.append(NoEscape(r"\clearpage"))

        if not self.job_data:
            raise ValueError("Job data not found")
            return
        d_job = self.job_data["job"]

        self.doc.append(NoEscape(r"\recipient{" + d_job["company_name"] + "}" + "{" + d_job["company_address"] + "}"))
        self.doc.append(NoEscape(r"\date{" + r"\today" + "}"))
        self.doc.append(NoEscape(r"\opening{" + d_job["cover_letter"]["opening"] + "," + "}"))
        self.doc.append(NoEscape(r"\closing{" + d_job["cover_letter"]["closing"] + "," + "}"))
        self.doc.append(NoEscape(r"\makeatletter"))
        self.doc.append(NoEscape(r"\let\@extrainfo\relax"))
        self.doc.append(NoEscape(r"\makelettertitle"))
        self.doc.append(NoEscape(r"\justifying{" + d_job["cover_letter"]["body"] + "\n" + r"\vspace{3mm}" + "}"))
        self.doc.append(NoEscape(r"\makeletterclosing"))

        self.doc.generate_pdf(self.save_path.as_posix() + "/cover_letter", clean_tex=False)

    def generate_cv_cover_letter(self):
        self.start_document()
        self.output_type = "CV_CL"
        self.generate_cv()
        self.generate_cover_letter()

    def generate_pdf(self, file_name: str = None):
        if file_name is None:
            file_name = self.candidate_data["profile"]["name"].replace(" ", "_")
        path_save_file = self.save_path / self.output_type / (file_name + f"_{self.output_type}")
        path_save_file.parent.mkdir(parents=True, exist_ok=True)
        self.doc.generate_pdf(path_save_file, clean_tex=False)
