import pandas as pd
from utilities import util, pageable


class SearchView(pageable.Pageable):
    _excluded_columns = ["Attachments"]

    def __init__(self) -> None:
        super().__init__()

        self._commands.register_cmd(
            "view",
            "view <message_id>` para expandir un mensaje",
            self._view_message_cmd,
        )

    def start_from_df(self, result_df: pd.DataFrame, search_text: str) -> None:
        util.clear_screen()

        if not result_df.empty:
            self._pageable_df = result_df

            self.pageable_start(f"Search result for `{search_text}`")

        else:
            print("No se encontraron resultados.")

            util.press_any_key()

    def _view_message_cmd(self, args: list[str]) -> None:
        message_id = "".join(args)

        if message_id and self._pageable_df is not None:
            if message_id in self._pageable_df["MessageID"]:
                target_message = self._pageable_df.loc[message_id]

                print(f"\nTimestamp: {target_message['Timestamp']}")
                print(f"Contents: {target_message['Contents']}")
                print(f"Attachments: {target_message['Attachments']}", end="\n\n")

                util.press_any_key()

                self._print_page()

            else:
                print(f"Introduce un `message_id` q exista y sea válido: {message_id}")

        else:
            print("Incluye el `message_id` luego del comando: `open <message_id>`")
