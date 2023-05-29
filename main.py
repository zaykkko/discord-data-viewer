"""
Main file :thumbs_up:
"""
import sys
import settings
from views.channels import ChannelsView
from views.game_stats import GameStatsView

if __name__ == "__main__":
    if len(sys.argv) > 1:
        BASE_DIR = settings.DEFAULT_BASE_DIR if len(sys.argv) < 2 else sys.argv[2]

        match sys.argv[1]:
            case "msgs" | "messages" | "channels":
                channels_view = ChannelsView(BASE_DIR)
                channels_view.start()

            case "stats":
                stats_view = GameStatsView(BASE_DIR)
                stats_view.start()

            case _:
                print("Huh?")

    else:
        print("At least input 1 arg: `[stats, msgs] <path/to/package>`")
