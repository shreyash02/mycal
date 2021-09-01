from abc import ABCMeta

from constants import MeetingAcceptanceStatus, BookingStatus


class User(object):
    def __init__(self, name):
        self.name = name
        self.calendar = UserCalendar(self)


class Event(object, metaclass=ABCMeta):
    def __init__(self, id, title, start, end):
        self.id = id
        self.title = title
        self.start = start
        self.end = end


class Meeting(Event):
    last_used_id = 0

    def __init__(self, id, owner, title, start, end, participants=None, room=None):
        super().__init__(id, title, start, end)
        self.owner = owner
        self.room = room

    def add_room(self, room):
        self.room = room


class Location(object):
    def __init__(self, name):
        self.name = name


class Room(Location):
    def __init__(self, name, number):
        super().__init__(name=name)
        self.number = number


class UserCalendar(object):

    def __init__(self, user):
        self.user = user
        self.event_list = []
        self.meeting_to_user_meeting_map = {}

    def add(self, user_event_participation):
        self.event_list.append(user_event_participation)
        self.event_list.sort(key=lambda e: e.meeting.start)
        self.meeting_to_user_meeting_map[user_event_participation.meeting] = user_event_participation

    @staticmethod
    def accept(user_event_participation):
        print("User {} is accepting the meeting {}".format(user_event_participation.user,
                                                           user_event_participation.meeting))
        user_event_participation.acceptance_status = MeetingAcceptanceStatus.ACCEPTED

    @staticmethod
    def decline(user_event_participation):
        user_event_participation.acceptance_status = MeetingAcceptanceStatus.DECLINED

    def get_user_meeting(self, meeting):
        return self.meeting_to_user_meeting_map.get(meeting)


class UserMeetingParticipation(object):
    def __init__(self, user, meeting, acceptance_status=None):
        self.user = user
        self.meeting = meeting

        if acceptance_status is None:
            self.acceptance_status = MeetingAcceptanceStatus.NO_RESPONSE
        else:
            self.acceptance_status = acceptance_status


class RoomBooking(object):
    def __init__(self, room, meeting):
        self.room = room
        self.meeting = meeting


class BookingResponse(object):
    def __init__(self, status=BookingStatus.FAILED, meeting=None):
        self.status = status
        self.meeting = meeting

