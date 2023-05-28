from abc import ABC
from math import floor
from typing import Union, Optional
from pandas import DataFrame

import settings
from .util import clear_screen
from .commands import CommandsMenu


class Pageable(ABC):
    _pageable_df: Union[DataFrame, None] = None  # protected
    _excluded_columns: list[str] = []

    def __init__(self) -> None:
        self._commands = CommandsMenu()

        self._sliced_df: Union[DataFrame, None] = None

        self._current_page = 0
        self._max_pages = 0

        self._page_cursor = 0
        self._page_cursor_offset = 0

        self._additional_info: Union[str, None] = None

        # basic pageable cmds hehe
        self._commands.register_cmd(
            "next", "Para ir a la siguiente página", self._next_page
        )
        self._commands.register_cmd(
            "prev", "Para ir a la anterior página", self._prev_page
        )

    def pageable_start(self, additional_info: Optional[str] = None) -> None:
        if self._pageable_df is not None:
            if additional_info:
                self._additional_info = additional_info

            self._reset_pageable_state()

            self._print_page()

            self._commands.start_menu()

        else:
            print("Unable to start view because of errors.")

    def get_pageabe_df(self) -> Union[DataFrame, None]:
        return self._pageable_df.copy() if self._pageable_df is not None else None

    def _reset_pageable_state(self) -> None:
        if self._pageable_df is not None:
            self._current_page = 0
            self._max_pages = floor(
                self._pageable_df.shape[0] / settings.MAX_ROWS_PER_PAGE
            )

            self._page_cursor = 0
            self._page_cursor_offset = settings.MAX_ROWS_PER_PAGE

            self._slice_df()

        else:
            raise ValueError("_pageable_df was not defined with a valid value.")

    def _next_page(self, _: Optional[list[str]] = None) -> None:
        if self._pageable_df is not None:
            if self._page_cursor_offset < self._pageable_df.shape[0]:
                self._current_page = min(self._current_page + 1, self._max_pages)

                self._page_cursor = self._page_cursor_offset

                self._page_cursor_offset = min(
                    self._page_cursor_offset + settings.MAX_ROWS_PER_PAGE,
                    self._pageable_df.shape[0],
                )

                self._slice_df()

            self._print_page()

        else:
            raise ValueError("_pageable_df was not defined with a valid value.")

    def _prev_page(self, _: Optional[list[str]] = None) -> None:
        if self._pageable_df is not None:
            if self._page_cursor_offset > settings.MAX_ROWS_PER_PAGE:
                self._current_page = max(self._current_page - 1, 0)

                cursor_offset_diff = self._page_cursor_offset - self._page_cursor

                self._page_cursor = max(
                    0, self._page_cursor - settings.MAX_ROWS_PER_PAGE
                )

                self._page_cursor_offset = max(
                    settings.MAX_ROWS_PER_PAGE,
                    self._page_cursor_offset - cursor_offset_diff,
                )

                self._slice_df()

            self._print_page()

        else:
            raise ValueError("_pageable_df was not defined with a valid value.")

    def _slice_df(self) -> None:
        if self._pageable_df is not None:
            self._sliced_df = self._pageable_df[
                self._page_cursor : self._page_cursor_offset
            ]

    def _print_page(self) -> None:
        if self._sliced_df is not None:
            clear_screen()

            modified_df = (
                self._sliced_df
                if not self._excluded_columns
                else self._sliced_df.drop(columns=self._excluded_columns)
            )

            print(modified_df)
            print(f"Page {self._current_page} of {self._max_pages}")

            if self._additional_info:
                print(self._additional_info)

        else:
            raise ValueError("_pageable_df was not defined with a valid value.")
