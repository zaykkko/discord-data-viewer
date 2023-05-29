import os
from typing import Union
import pandas as pd

import settings
from utilities import util, pageable
from .messages import MessagesView


class ChannelsView(pageable.Pageable):
    def __init__(self, base_dir: str):
        super().__init__()

        self._base_dir = util.get_base_dir(base_dir)
        self._msgs_view = MessagesView(self._base_dir)

        msgs_index_path = os.path.join(
            self._base_dir, settings.MESSAGES_DIR, settings.MESSAGES_INDEX_FILE
        )

        try:
            exported_channels = util.load_json(msgs_index_path)

            self._pageable_df = pd.DataFrame(
                list(exported_channels.items()),
                columns=["channel_id", "display_name"],
                dtype=str,
            )
            self._pageable_df.set_index("channel_id", inplace=True)

        except OSError:
            print(
                f"File or folder doesn't exists, check it out in the '{msgs_index_path}' folder."
            )

        self._commands.register_cmd(
            "open", "open <channel_id>` para ir al canal", self._open_message_cmd
        )

    def start(self) -> None:
        self.pageable_start()

    def get_channels(
        self,
    ) -> Union[None, pd.DataFrame]:  # el return type ya es implícito... pero bueno
        return None if self._pageable_df is None else self._pageable_df.copy()

    def _open_message_cmd(self, args: list[str]) -> None:
        channel_id = "".join(args)

        if channel_id and self._pageable_df is not None:
            print("Espera...")

            if channel_id in self._pageable_df.index and self._msgs_view.load_messages(
                channel_id
            ):
                self._msgs_view.start()

                self._print_page()

            else:
                print(f"Ese `channel_id` no existe: {channel_id}")

        else:
            print(
                f"Incluye el `channel_id` luego del comando `open <channel_id>`: {channel_id}"
            )
