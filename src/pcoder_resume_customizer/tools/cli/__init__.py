import typer

from pcoder_resume_customizer import settings

cli = typer.Typer(
    invoke_without_command=True,
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_enable=settings.typer.enable_pretty_exception,
    pretty_exceptions_show_locals=settings.typer.show_pretty_exception_local,
)


@cli.callback()
def default_callback(ctx: typer.Context):
    pass


if __name__ == "__main__":
    cli()
