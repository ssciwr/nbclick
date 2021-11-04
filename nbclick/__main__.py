import click
import nbclient
import nbformat
import nbparameterise


class NotebookCommandClass(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            subcommand_metavar="NOTEBOOK [OPTIONS]...",
            options_metavar="",
        )

    def get_command(self, ctx, name):
        # Read the notebook
        with open(name) as f:
            nb = nbformat.read(f, as_version=4)

        # Extract parameters from the notebook
        click_params = []
        old_params = nbparameterise.extract_parameters(nb)
        for param in old_params:
            # Create a help text from the given comment
            help = param.comment
            if help is not None:
                # This removes the '#' from the comment
                help = help[1:].strip()

            # Create a click option from the given parameter
            click_params.append(
                click.Option(
                    (f"--{param.name}",),
                    default=param.value,
                    type=param.type,
                    show_default=True,
                    help=help,
                )
            )

        def callback(**parameters):
            new_params = nbparameterise.parameter_values(old_params, **parameters)
            new_nb = nbparameterise.replace_definitions(nb, new_params)
            nbclient.execute(new_nb)

        return click.Command(name, params=click_params, callback=callback)


@click.command(cls=NotebookCommandClass)
def main():
    pass


if __name__ == "__main__":
    main()
