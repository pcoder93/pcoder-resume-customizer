# Pcoder Resume Customizer

Create a resume and cover letter for a job application from a yaml [profile](Applications/profile.yaml) and [job details](Applications/job_details.yml).

## Quick Start 

1. Clone the repository to your local machine.
    ```bash
    git clone https://github.com/pcoder93/pcoder-resume-customizer.git
    cd pcoder-resume-customizer
    ```
2. Create virtual environment and install dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    poetry install
    ```
    or conda.
    ```bash
    conda create -n py312_prc python=3.12
    conda activate py312_prc
    poetry install
    ```
3. Modify the [profile](Applications/profile.yaml) and [job details](Applications/job_details.yml) files as needed and add a [headshot](Applications/headshot.png) if you want
4. Run the CLI.
    ```bash
    prc create_cv_cover_letter --profile profile.yaml --job_details job_details.yml
    ```
If everything goes well, you should see the a new folder with the job details in the [Applications](Applications) folder.

## All commands

```bash
# if you want to create a CV only
prc create-cv --profile <path to profile.yml> 
# if you want to create a cover letter only
prc create-cover-letter --profile <path to profile.yml> --job-details <path to job_details.yml> 
# if you want to create both
prc create-cv-cover-letter --profile <path to profile.yml> --job-details <path to job_details.yml> 
```
