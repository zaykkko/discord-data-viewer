"""
Main file :thumbs_up:
"""
import sys
import settings
from views.channels import ChannelsView

if __name__ == "__main__":
    channels_view = ChannelsView(
        settings.DEFAULT_BASE_DIR if len(sys.argv) < 0 else sys.argv[1]
    )
    channels_view.start()
