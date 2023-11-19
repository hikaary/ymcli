from random import random

from yandex_music import ClientAsync, StationResult, Track


class Radio:
    def __init__(self, client: ClientAsync):
        self.client: ClientAsync = client
        self.station_id: str | None = None
        self.station_from = None

        self.play_id: str | None = None
        self.index = 0
        self.current_track: Track | None = None
        self.station_tracks = None

    async def get_all_stations(self) -> list[StationResult]:
        stations = await self.client.rotor_stations_list()
        available_stations = []
        for station in stations:
            if station.rup_description:
                available_stations.append(station)
        return available_stations

    async def get_first_track(self, station_id, station_from) -> Track:
        self.station_id = station_id
        self.station_from = station_from

        await self.__update_radio_batch()
        self.current_track = await self.__update_current_track()

        return self.current_track

    async def get_next_track(self) -> Track:
        assert (
            self.current_track is not None
            and self.play_id is not None
            and self.station_tracks is not None
        )

        await self.__send_play_end_track(
            self.current_track,
            self.play_id,
        )
        await self.__send_play_end_radio(
            self.current_track,
            self.station_tracks.batch_id,
        )

        self.index += 1
        if self.index >= len(self.station_tracks.sequence):
            await self.__update_radio_batch(
                self.current_track.track_id,
            )

        self.current_track = None
        while self.current_track is None:
            await self.__update_current_track()

        return self.current_track

    async def __update_radio_batch(self, queue: int | str | bool = False):
        self.index = 0
        assert self.station_id is not None

        self.station_tracks = await self.client.rotor_station_tracks(
            self.station_id,
            queue=queue,  # type: ignore
        )
        await self.__send_start_radio(self.station_tracks.batch_id)

    async def __update_current_track(self):
        self.play_id = self.__generate_play_id()
        track_id = self.station_tracks.sequence[self.index].track.track_id
        tracks = await self.client.tracks([track_id])
        track = tracks[0]
        await self.__send_play_start_track(track, self.play_id)
        await self.__send_play_start_radio(track, self.station_tracks.batch_id)
        return track

    async def __send_start_radio(self, batch_id):
        assert self.station_from is not None and self.station_id is not None

        await self.client.rotor_station_feedback_radio_started(
            station=self.station_id,
            from_=self.station_from,
            batch_id=batch_id,
        )

    async def __send_play_start_track(self, track, play_id):
        total_seconds = track.duration_ms / 1000
        await self.client.play_audio(
            from_="desktop_win-home-playlist_of_the_day-playlist-default",
            track_id=track.id,
            album_id=track.albums[0].id,
            play_id=play_id,
            track_length_seconds=0,
            total_played_seconds=0,
            end_position_seconds=total_seconds,
        )

    async def __send_play_start_radio(self, track, batch_id):
        assert self.station_id is not None

        await self.client.rotor_station_feedback_track_started(
            station=self.station_id,
            track_id=track.id,
            batch_id=batch_id,
        )

    async def __send_play_end_track(self, track: Track, play_id: str):
        played_seconds = track.duration_ms / 1000  # type: ignore
        total_seconds = track.duration_ms / 1000  # type: ignore
        await self.client.play_audio(
            from_="desktop_win-home-playlist_of_the_day-playlist-default",
            track_id=track.id,
            album_id=track.albums[0].id,  # type: ignore
            play_id=play_id,
            track_length_seconds=int(total_seconds),
            total_played_seconds=played_seconds,
            end_position_seconds=total_seconds,
        )

    async def __send_play_end_radio(
        self,
        track: Track,
        batch_id: str,
    ):
        played_seconds = track.duration_ms / 1000  # type: ignore
        assert self.station_id is not None
        await self.client.rotor_station_feedback_track_finished(
            station=self.station_id,
            track_id=track.id,
            total_played_seconds=played_seconds,
            batch_id=batch_id,
        )

    @staticmethod
    def __generate_play_id():
        return "%s-%s-%s" % (
            int(random() * 1000),
            int(random() * 1000),
            int(random() * 1000),
        )
