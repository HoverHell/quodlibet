# -*- coding: utf-8 -*-
# Copyright 2012-2015 Ryan "ZDBioHazard" Turner <zdbiohazard2@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import math
import random

from quodlibet.plugins.playorder import PlayOrderPlugin, PlayOrderShuffleMixin


class PlaycountEqualizer(PlayOrderPlugin, PlayOrderShuffleMixin):
    PLUGIN_ID = "playcounteq"
    PLUGIN_NAME = _("Playcount Equalizer")
    PLUGIN_DESC = _("This shuffle play order plugin selects the next song "
                    "weighted inversely by ~#playcount. Attempting to "
                    "equalize the ~#playcount of all songs in the playlist."
                    "\n\n"
                    "This might be useful when you have new songs that you "
                    "aren't tired of yet; They will be played more often than "
                    "songs you've had for a while and have heard many times."
                    "\n\n"
                    "Note: In some cases, the same song can be played "
                    "multiple times in a row. This usually happens in small "
                    "playlists with large ~#playcount divides.")
    PLUGIN_ICON = "gtk-refresh"
    PLUGIN_VERSION = "1.0"

    # Select the previous track.
    def previous(self, playlist, current):
        return super(PlaycountEqualizer, self).previous(playlist, current)

    # Select the next track.
    def next(self, playlist, current):
        super(PlaycountEqualizer, self).next(playlist, current)

        songs = playlist.get()
        # Don't try to search through an empty playlist.
        if len(songs) <= 0:
            return None

        # Set-up the search information.
        max_count = max([song('~#playcount') for song in songs])
        weights = [max_count - song('~#playcount') for song in songs]
        choice = int(max(1, math.ceil(sum(weights) * random.random())))

        # Search for a track.
        for i, weight in enumerate(weights):
            choice -= weight
            if choice <= 0:
                return playlist.get_iter([i])
        else:  # This should only happen if all songs have equal play counts.
            return playlist.get_iter([random.randint(0, len(songs) - 1)])
