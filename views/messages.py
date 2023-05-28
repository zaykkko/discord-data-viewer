from os import path
from typing import Union
from json import JSONDecodeError
import pandas as pd

import settings
from dtypes import ChannelInfo
from utilities import util, pageable
from .search import SearchView


class MessagesView(pageable.Pageable):
    _excluded_columns = ["Attachments"]

    def __init__(self, base_dir: str):
        super().__init__()

        self._base_dir = base_dir
        self._channel_info: Union[ChannelInfo, None] = None

        self._search_view = SearchView()

        self._commands.register_cmd(
            "view",
            "view <message_id>` para expandir un mensaje",
            self._view_message_cmd,
        )
        self._commands.register_cmd(
            "search",
            "search <some text>` para buscar mensajes q contengan esa porción de texto",
            self._search_text_cmd,
        )

    def start(self) -> None:
        self.pageable_start()

    def get_channel_info(self) -> Union[ChannelInfo, None]:
        return None if self._channel_info is None else self._channel_info.copy()

    def get_msgs_df(self) -> Union[pd.DataFrame, None]:
        return self._pageable_df.copy() if self._pageable_df is not None else None

    def load_messages(self, channel_id: str) -> bool:
        if self._channel_info and self._channel_info["id"] == channel_id:
            channel_dir = util.get_channel_dir(self._base_dir, channel_id)

            messages_csv_file = path.join(channel_dir, settings.MESSAGES_CSV_FILE)

            try:
                self._pageable_df = pd.read_csv(messages_csv_file, dtype=str)

                # rename index column
                self._pageable_df.rename(columns={"ID": "MessageID"}, inplace=True)
                self._pageable_df.set_index("MessageID", inplace=True)

                # change timestamp dtype, change format and sort rows by it (ascending way)
                self._pageable_df["Timestamp"] = pd.to_datetime(
                    self._pageable_df["Timestamp"], format="ISO8601"
                )
                self._pageable_df["Timestamp"] = self._pageable_df[
                    "Timestamp"
                ].dt.strftime("%Y-%m-%d %H:%M:%S")
                self._pageable_df.sort_values(by="Timestamp", inplace=True)

                # self._msgs_df.drop(columns=['Attachments'], inplace=True)

                return True

            except (IOError, pd.errors.ParserError):
                print(
                    "Messages CSV file from channel not found or has an invalid format, "
                    f"take a look in {messages_csv_file}."
                )

        if (
            not self._channel_info or self._channel_info["id"] != channel_id
        ) and self._load_channel_info(channel_id):
            return self.load_messages(channel_id)

        return False

    def _load_channel_info(self, channel_id: str) -> bool:
        channel_info_path = path.join(
            util.get_channel_dir(self._base_dir, channel_id), settings.CHANNEL_INFO_FILE
        )

        try:
            self._channel_info = util.load_json(channel_info_path)

            return True

        except (OSError, JSONDecodeError):
            print(
                f"Channel info file doesn't exists, check it out in {channel_info_path} folder."
            )

        return False

    def _view_message_cmd(self, args: list[str]) -> None:
        message_id = "".join(args)

        if message_id and self._pageable_df is not None:
            if message_id in self._pageable_df.index:
                target_message = self._pageable_df.loc[message_id]

                print(f"\nTimestamp: {target_message['Timestamp']}")
                print(f"Contents: {target_message['Contents']}")
                print(
                    f"Attachments: {target_message['Attachments']}",
                    end="\n\n",
                )

                util.press_any_key()

                self._print_page()

            else:
                print(f"Introduce un `message_id` q exista y sea válido: {message_id}")

        else:
            print("Incluye el `message_id` luego del comando: `open <message_id>`")

    def _search_text_cmd(self, args: list[str]) -> None:
        search_text = " ".join(args)

        if search_text and self._pageable_df is not None:
            filtered_na_df = self._pageable_df.dropna(subset=["Contents"])

            search_result_df = filtered_na_df["Contents"].str.contains(search_text)

            found_msgs_df = filtered_na_df[search_result_df]

            self._search_view.start_from_df(found_msgs_df, search_text)

            self._print_page()

        else:
            print("Incluye el texto luego del comando: `search <some text>`")
