import os
from importlib import util, import_module
import click


class TreeCommands:
    def __init__(self):
        self.load_commands()
        # Invoke the CLI only after loading all commands and subcommands
        self.cli()

    @staticmethod
    @click.group()
    def cli():
        pass

    def load_commands(self):
        # Iterate over subdirectories in the specified folder
        folder_path = os.path.join(os.getcwd(), "cli")

        for item in os.listdir(folder_path):
            if not item.startswith("__") and os.path.isdir(
                os.path.join(folder_path, item)
            ):
                # Form the module path using the directory name
                module_path = os.path.join(folder_path, item, "__init__.py")

                # Check if the module path exists
                if os.path.exists(module_path):
                    # Create a spec for the module
                    spec = util.spec_from_file_location(f"cli.{item}", module_path)

                    # Check if the spec is not None before creating the module
                    if spec is not None:
                        module = util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        # Now, 'module' contains the imported module
                        # You can use 'module' as needed

                        # Check if the module has a 'cli' attribute with a 'name' attribute
                        command = getattr(module, item, None)

                        # Load subcommands
                        for file in os.listdir(os.path.join(folder_path, item)):
                            if not file.startswith("__") and file.endswith(".py"):
                                subcommand_name = file[:-3]  # Remove the ".py" extension
                                subcommand_path = os.path.join(folder_path, item, file)

                                try:
                                    # Import the subcommand module
                                    subcommand_module = import_module(f"cli.{item}.{subcommand_name}")

                                    # Find the subcommand function
                                    subcommand_func = getattr(subcommand_module, subcommand_name, None)

                                    if subcommand_func is not None:
                                        print(f"Subcommand: {subcommand_name}, Path: {subcommand_path}, Module: {subcommand_module}, Command: {subcommand_func}")
                                        command.add_command(subcommand_func)
                                    else:
                                        print(f"Subcommand function not found in {subcommand_path}")

                                        # Print the content of the subcommand module
                                        print(f"Subcommand Module Content: {dir(subcommand_module)}")

                                except ImportError as e:
                                    print(f"Error importing module {subcommand_path}: {e}")

                        # Add the command to the main group (cli)
                        self.cli.add_command(command)

                    else:
                        print(f"Spec is None for {item}")


if __name__ == "__main__":
    TreeCommands()
