import os
import sys
from importlib import import_module
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
        # Get the current working directory
        current_directory = os.getcwd()

        # Add the current directory to sys.path
        sys.path.append(current_directory)

        # Iterate over subdirectories in the specified folder
        folder_path = os.path.join(current_directory, "cli")

        for item in os.listdir(folder_path):
            if not item.startswith("__") and os.path.isdir(
                os.path.join(folder_path, item)
            ):
                # Form the module path using the directory name
                module_path = f"cli.{item}"

                try:
                    # Import the module
                    module = import_module(module_path)

                    # Check if the module has a 'cli' attribute with a 'name' attribute
                    command = getattr(module, item, None)

                    # Load subcommands
                    for file in os.listdir(os.path.join(folder_path, item)):
                        if not file.startswith("__") and file.endswith(".py"):
                            subcommand_name = file[:-3]  # Remove the ".py" extension
                            subcommand_path = f"cli.{item}.{subcommand_name}"

                            try:
                                # Import the subcommand module
                                subcommand_module = import_module(subcommand_path)

                                # Find the subcommand function
                                subcommand_func = getattr(subcommand_module, subcommand_name, None)

                                if subcommand_func is not None:
                                    command.add_command(subcommand_func)
                                else:
                                    print(f"Subcommand function not found in {subcommand_path}")

                                    # Print the content of the subcommand module
                                    print(f"Subcommand Module Content: {dir(subcommand_module)}")

                            except ImportError as e:
                                print(f"Error importing module {subcommand_path}: {e}")

                    # Add the command to the main group (cli)
                    self.cli.add_command(command)

                except ImportError as e:
                    print(f"Error importing module {module_path}: {e}")

        # Remove the current directory from sys.path to avoid interference
        sys.path.remove(current_directory)


if __name__ == "__main__":
    TreeCommands()
