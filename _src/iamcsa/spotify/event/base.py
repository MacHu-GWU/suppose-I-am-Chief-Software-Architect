# -*- coding: utf-8 -*-

class BaseEvent(object):
    def put_record_to_kinesis_stream(self, aws_profile, stream_name):
        pass


class SubscribeSpotify(BaseEvent): pass


class UnsubscribeSpotify(BaseEvent): pass


class SignUp(BaseEvent): pass


class SignIn(BaseEvent): pass


class SignOut(BaseEvent): pass


class PlayMusic(BaseEvent): pass


class PlayAlbum(BaseEvent): pass


class PlayPlaylist(BaseEvent): pass


class Pause(BaseEvent): pass


class KillApp(BaseEvent): pass


class GoRadio(BaseEvent): pass
