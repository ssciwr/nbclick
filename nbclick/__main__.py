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
            # Create the name of the flag
            flag = f"--{param.name}"
            if issubclass(param.type, bool):
                flag = f"--{param.name}/--no-{param.name}"

            # A dictionary of arguments to click.Option
            opt_args = {}

            # Default values can bet taken directly from param. We
            # always display the defaults in --help
            opt_args["default"] = param.value
            opt_args["show_default"] = True

            # If the parameter is a list we need to inspect the default
            # for type information.
            if issubclass(param.type, list):
                types = tuple(type(item) for item in param.value)
                if len(set(types)) == 1:
                    # This is a list of a single type, we realize it by click's
                    # nargs option. click does not support variable length list parameters
                    # because they result in ambiguous parser behaviour
                    opt_args["nargs"] = len(param.value)
                    opt_args["type"] = types[0]
                else:
                    # For multi-type lists, we require all types to be present
                    opt_args["type"] = types
            else:
                # Type information for scalar types can be taken from param
                opt_args["type"] = param.type

            # Create a help text from the given comment
            opt_args["help"] = param.comment
            if param.comment is not None:
                # This removes the '#' from the comment
                opt_args["help"] = param.comment[1:].strip()

            # Create a click option from the given parameter
            click_params.append(click.Option((flag,), **opt_args))

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
