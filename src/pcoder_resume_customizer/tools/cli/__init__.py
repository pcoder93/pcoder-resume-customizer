import typer

from pcoder_resume_customizer import settings
from pcoder_resume_customizer.moderncv import ModernCV

cli = typer.Typer(
    invoke_without_command=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_enable=settings.typer.enable_pretty_exception,
    pretty_exceptions_show_locals=settings.typer.show_pretty_exception_local,
)


@cli.command(no_args_is_help=True)
def create_cv(
    profile: str,
    job_details: str = None,
    save_path: str = None,
    save_name: str = None,
):
    """
    Create a CV

    Args:
        profile (str): Path to the profile YAML file
        job_details (str): Path to the job details YAML file
        save_path (str): Path to save the CV
        save_name (str): Name of the output file PDF (without extension)
    """
    new_cv = ModernCV(profile, job_details, save_path)
    new_cv.generate_cv()
    new_cv.generate_pdf(save_name)


@cli.command(no_args_is_help=True)
def create_cover_letter(
    profile: str,
    job_details: str = None,
    save_path: str = None,
    save_name: str = None,
):
    """
    Create a Cover Letter

    Args:
        profile (str): Path to the profile YAML file
        job_details (str): Path to the job details YAML file
        save_path (str): Path to save the CV
        save_name (str): Name of the output file PDF (without extension)
    """
    new_cv = ModernCV(profile, job_details, save_path)
    new_cv.generate_cover_letter()
    new_cv.generate_pdf(save_name)


@cli.command(no_args_is_help=True)
def create_cv_cover_letter(
    profile: str,
    job_details: str = None,
    save_path: str = None,
    save_name: str = None,
):
    """
    Create a CV and Cover Letter

    Args:
        profile (str): Path to the profile YAML file
        job_details (str): Path to the job details YAML file
        save_path (str): Path to save the CV
        save_name (str): Name of the output file PDF (without extension)
    """
    new_cv = ModernCV(profile, job_details, save_path)
    new_cv.generate_cv_cover_letter()
    new_cv.generate_pdf(save_name)


@cli.callback()
def default_callback(ctx: typer.Context):
    pass


if __name__ == "__main__":
    cli()
