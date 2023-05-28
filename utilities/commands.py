from typing import Callable, Optional


class CommandsMenu:
    def __init__(self) -> None:
        self._commands: dict[str, tuple[str, Callable[..., None]]] = {}

        self._menu_stopped = False

        self.register_cmd("exit", "Para salir", self.stop_menu)

    def register_cmd(
        self, name: str, description: str, callback: Callable[..., None]
    ) -> bool:
        if name not in self._commands:
            self._commands[name] = (description, callback)

            return True

        return False

    def unregister_command(self, name: str) -> bool:
        if name in self._commands:
            del self._commands[name]

            return True

        return False

    def start_menu(self) -> None:
        self._menu_stopped = False

        self._menu_loop()

    def stop_menu(self, _: Optional[list[str]] = None) -> None:
        self._menu_stopped = True

    def print_commands(self) -> None:
        print("\nCommand list: what now?")

        for cmd_name, (description, _) in self._commands.items():
            print(f"* {cmd_name} - {description}")

    def _menu_loop(self) -> None:
        while not self._menu_stopped:
            self.print_commands()

            input_cmd, *args = input("Ingrese el comando: ").split(" ")

            if input_cmd.lower() in self._commands:
                self._execute_command(input_cmd.lower(), args)

            else:
                print("Introduce alguno de los de arriba POR FAVOR.")

    def _execute_command(self, name: str, args: list[str]) -> None:
        _, function = self._commands[name]

        function(args)
