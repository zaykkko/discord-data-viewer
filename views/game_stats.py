import os
import requests
import pandas as pd

from utilities import util, pageable
import settings


class GameStatsView(pageable.Pageable):
    def __init__(self, base_dir: str):
        super().__init__()

        self._base_dir = util.get_base_dir(base_dir)

        apps_request = requests.get(settings.DISCORD_APPS_ENDPOINT, timeout=15)

        if apps_request.status_code == 200:
            self._apps_df = pd.DataFrame(apps_request.json())

            user_data_path = os.path.join(self._base_dir, settings.USER_DATA_FILE)

            try:
                self._user_data = util.load_json(user_data_path)

                if "user_activity_application_statistics" in self._user_data:
                    user_activity_df = pd.DataFrame(
                        self._user_data["user_activity_application_statistics"],
                        dtype=str,
                    )

                    self._pageable_df = pd.merge(
                        user_activity_df,
                        self._apps_df[["id", "name"]],
                        left_on="application_id",
                        right_on="id",
                        how="left",
                    )
                    self._pageable_df.rename(
                        columns={
                            "name": "app_name",
                            "application_id": "app_id",
                            "total_duration": "total_time",
                            "last_played_at": "last_played",
                        },
                        inplace=True,
                    )
                    self._pageable_df.set_index("app_id", inplace=True)

                    self._pageable_df["app_name"].fillna(
                        "[Not detected by Discord, custom presence]", inplace=True
                    )

                    self._pageable_df["total_time"] = pd.to_datetime(
                        self._pageable_df["total_time"].astype(int), unit="s"
                    ).dt.strftime("%H:%M:%S")
                    self._pageable_df.sort_values(
                        by="total_time", ascending=False, inplace=True
                    )

                    self._pageable_df.drop(
                        columns=["id", "total_discord_sku_duration"], inplace=True
                    )

                    self._pageable_df["last_played"] = pd.to_datetime(
                        self._pageable_df["last_played"], format="ISO8601"
                    )
                    self._pageable_df["last_played"] = self._pageable_df[
                        "last_played"
                    ].dt.strftime("%Y-%m-%d %H:%M:%S")

                    columns_pos = list(range(self._pageable_df.shape[1]))
                    columns_pos[1], columns_pos[-1] = columns_pos[-1], columns_pos[1]

                    self._pageable_df = self._pageable_df.iloc[:, columns_pos]

                else:
                    print("Unable to get activity statistics from user data file.")

            except OSError:
                print(
                    f"File or folder doesn't exists, check it out in the '{user_data_path}' folder."
                )

        else:
            print("Unable to get games from Discord's API.")

        self._commands.register_cmd(
            "app", "App id by <some name>", self._find_id_by_name_cmd
        )

    def start(self) -> None:
        self.pageable_start()

    def _find_id_by_name_cmd(self, args: list[str]) -> None:
        search_text = " ".join(args).lower()

        if self._apps_df is not None:
            search_result_df = (
                self._apps_df["name"].str.lower().str.contains(search_text)
            )

            id_name_df = self._apps_df[["id", "name"]][search_result_df]
            icon_type_df = self._apps_df[["icon", "type"]][search_result_df]

            util.clear_screen()

            print(id_name_df)
            print(icon_type_df)

            util.press_any_key()

            self._print_page()
