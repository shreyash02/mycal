import datetime

import pytz

from models import User, Room, Meeting, BookingResponse, RoomBooking, UserMeetingParticipation

from constants import MeetingAcceptanceStatus, BookingStatus

from utils import get_user_readable_datetime, get_user_readable_duration, filter_free_slots


class MeetingScheduler(object):
    @staticmethod
    def schedule(calendar_system, owner, title, start, end, participants=None, room=None):
        if room:
            # Check if the room is available
            for room_booking in calendar_system.room_booking_list:
                used_room = room_booking.room

                if room == used_room:
                    print("Checking room: {} against {}".format(room, used_room))
                    meeting = room_booking.meeting
                    if not ((end <= meeting.start) or (start >= meeting.end)):
                        return BookingResponse(status=BookingStatus.FAILED)

            # Room is free, we can book

        # create meeting
        calendar_system.last_used_meeting_id += 1
        meeting_id = calendar_system.last_used_meeting_id
        new_meeting = Meeting(meeting_id, owner, title, start, end)

        if room:
            # add to room bookings
            new_meeting.add_room(room)
            calendar_system.room_booking_list.append(RoomBooking(room, new_meeting))
            calendar_system.room_booking_list.sort(key=lambda e: e.meeting.start)
            calendar_system.meeting_to_room_map[new_meeting] = room

        # add to all the participants' calendar
        owner.calendar.add(UserMeetingParticipation(meeting=new_meeting, user=owner,
                                                    acceptance_status=MeetingAcceptanceStatus.ACCEPTED))
        for participant in participants:
            participant.calendar.add(UserMeetingParticipation(meeting=new_meeting, user=participant))

        calendar_system.meeting_to_participants_map[new_meeting] = participants

        return BookingResponse(status=BookingStatus.SUCCESS, meeting=new_meeting)

    @staticmethod
    def update_meeting(calendar_system, meeting, title=None, start=None, end=None, participants=None, room=None):
        if meeting not in calendar_system.meeting_list:
            raise Exception("Meeting not found in the system")

        # if start, end or room is updated, check if we can still get the room for the changed time

        # Here

        # If all is well, then update the following if changed
        # title

        # change the calendar entry of the participants

        # if the time has changed, then move their acceptance status to NA

        if title:
            meeting.title = title

    @staticmethod
    def cancel_meeting():
        # Remove the entry from all participants calendars

        # Free up the room if this meeting had any

        # Remove the meeting from the meeting list
        pass

    @staticmethod
    def get_free_rooms(calendar_system, start, end):
        if start > end:
            raise Exception("Invalid input, start is after end")

        free_rooms = calendar_system.room_list.copy()

        for room_booking in calendar_system.room_booking_list:
            if room_booking.room in free_rooms:
                if not (end <= room_booking.meeting.start or start >= room_booking.meeting.end):
                    free_rooms.remove(room_booking.room)
                    if not free_rooms:
                        break

        return free_rooms


class CalendarSystem(object):
    def __init__(self):
        self.user_list = []
        self.room_list = []
        self.meeting_list = []

        self.room_booking_list = []

        self.last_used_user_id = 0
        self.last_used_room_id = 0
        self.last_used_meeting_id = 0

        self.meeting_to_participants_map = {}
        self.meeting_to_room_map = {}

    def create_users(self, user_count):
        for i in range(user_count):
            name = "User {}".format(i + 1)
            self.user_list.append(User(name))

        return self.user_list

    def create_rooms(self, room_count):
        for i in range(room_count):
            number = i + 1
            name = "Room {}".format(number)
            self.room_list.append(Room(name, number))

        return self.room_list

    def create_meeting(self, owner, title, start, end, participants=None, room=None):
        meeting_create_response = MeetingScheduler.schedule(self, owner, title, start, end,
                                                            participants=participants,
                                                            room=room)

        if meeting_create_response.status == BookingStatus.SUCCESS:
            return meeting_create_response.meeting

    def get_meeting_details(self, meeting):
        meeting_data = {"title": meeting.title,
                        "owner": meeting.owner.name,
                        "room": meeting.room}

        participants = self.meeting_to_participants_map[meeting]
        room = self.meeting_to_room_map.get(meeting)

        meeting_data["acceptance_status"] = {}
        for participant in participants:
            user_meeting = participant.calendar.meeting_to_user_meeting_map[meeting]
            meeting_data["acceptance_status"][participant] = user_meeting.acceptance_status

        return meeting_data

    def get_user_calendar(self, user, timezone=None):
        meetings_data = []
        for user_meeting in user.calendar.event_list:
            meeting = user_meeting.meeting

            start = pytz.utc.localize(meeting.start)
            end = pytz.utc.localize(meeting.end)

            if timezone:
                start = start.astimezone(timezone)
                end = end.astimezone(timezone)

            meeting_data = {
                "title": meeting.title,
                "owner": meeting.owner.name,
                "start": start,
                "end": end,
                "status": user_meeting.acceptance_status,
                "room": self.meeting_to_room_map.get(meeting).name
            }
            meetings_data.append(meeting_data)

        return meetings_data

    def print_user_calendar(self, user, timezone=None):
        user_calendar = self.get_user_calendar(user, timezone)
        print("Calendar of user {}:".format(user.name))
        print()

        for event in user_calendar:
            print("Title: {}".format(event["title"]))
            if event["owner"] == user.name:
                print("You created this meeting")
            else:
                print("Invited by: {}".format(event["owner"]))

            start_str = get_user_readable_datetime(event["start"])
            end_str = get_user_readable_datetime(event["end"])
            duration = event["end"] - event["start"]
            duration_str = get_user_readable_duration(duration)

            print("Start: {} End: {} ({})".format(start_str, end_str, duration_str))
            print("Room: {}".format(event["room"]))

            status_message = "not accepted or declined"
            if event["status"] == MeetingAcceptanceStatus.ACCEPTED:
                status_message = "accepted"
            elif event["status"] == MeetingAcceptanceStatus.DECLINED:
                status_message = "declined"

            print("You have {} this meeting".format(status_message))

            print("")

    def get_free_rooms(self, start, end):
        return MeetingScheduler.get_free_rooms(self, start, end)

    def get_free_room_slots(self, room, date):
        day_start = datetime.datetime.combine(date, datetime.datetime.min.time())
        day_end = day_start + datetime.timedelta(days=1)

        free_slots = [[day_start, day_end]]
        busy_slots = []

        for room_booking in self.room_booking_list:
            if room_booking.room == room and day_start.date() <= room_booking.meeting.start.date() < day_end.date():
                meeting = room_booking.meeting
                busy_slots.append([meeting.start, meeting.end])

        # print("Free slots: {}".format(free_slots))
        # print("Busy slots: {}".format(busy_slots))
        free_slots = filter_free_slots(free_slots, busy_slots)
        # print("New Free slots: {}".format(free_slots))

        return free_slots

    @staticmethod
    def get_user_busy_slots(user, date):
        events_on_date = []

        for event in user.calendar.event_list:
            if event.meeting.start.date() == date:
                events_on_date.append([event.meeting.start, event.meeting.end])

        return events_on_date

    def get_free_time_slots(self, users, room, date=None):
        if date is None:
            date = datetime.datetime.today()

        free_slots = self.get_free_room_slots(room, date)

        print("+++++++++++++++++++++++++++++++++++++++++ Starting for users ++++++++++++++++++++++++++++++++++++++++++")

        for user in users:
            # print(">>>> Current free slots:")
            # print(free_slots)

            if not free_slots:
                break

            user_busy_slots = self.get_user_busy_slots(user, date)
            # print("====>> User ({}) busy slots:".format(user.name))
            # print(user_busy_slots)
            free_slots = filter_free_slots(free_slots, user_busy_slots)
            # print("-" * 80)

        return free_slots
