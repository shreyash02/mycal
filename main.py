import datetime
import pprint

import pytz

from system import CalendarSystem

from models import Event


def main():
    system = CalendarSystem()

    user_list = system.create_users(10)
    system.create_rooms(3)

    # Create meeting #1
    meeting_title = "Morning catch-up"
    start = datetime.datetime(2021, 5, 4, 10, 0)
    end = datetime.datetime(2021, 5, 4, 11, 0)

    owner = user_list[0]
    participants = user_list[1:6]
    free_rooms = system.get_free_rooms(start, end)
    if free_rooms:
        room = free_rooms[0]
        meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                        room=room)
        print("Created meeting: {} with id: {}".format(meeting, meeting.id))
    else:
        print("No more rooms from {} to {}".format(start, end))
        return

    p0 = participants[0]
    p0_user_meeting = p0.calendar.get_user_meeting(meeting)
    p0.calendar.accept(p0_user_meeting)

    p2 = participants[2]
    p2_user_meeting = p2.calendar.get_user_meeting(meeting)
    p2.calendar.decline(p2_user_meeting)

    p4 = participants[4]
    p4_user_meeting = p4.calendar.get_user_meeting(meeting)
    p4.calendar.accept(p4_user_meeting)

    print("Details of meeting {}:".format(meeting.title))
    pprint.pprint(system.get_meeting_details(meeting))

    print("Calendar of user {}:".format(p0.name))
    pprint.pprint(system.get_user_calendar(p0))

    """ =========================== End of meeting #1 ============================== """

    meeting_title = "Stand-up meeting"
    owner = user_list[4]
    participants = user_list[1:7]
    start = datetime.datetime(2021, 5, 4, 11, 30)
    end = datetime.datetime(2021, 5, 4, 12, 0)

    free_rooms = system.get_free_rooms(start, end)
    if free_rooms:
        room = free_rooms[0]
        meeting2 = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                         room=room)
        print("Created meeting: {} with id: {}".format(meeting2, meeting2.id))
    else:
        print("No more rooms from {} to {}".format(start, end))

    print("Calendar of user {}:".format(p0.name))
    pprint.pprint(system.get_user_calendar(p0))

    free_rooms = system.get_free_rooms(start, end)
    print("Free rooms from {} to {}: {}".format(start, end, free_rooms))

    """ =========================== End of meeting #2 ============================== """

    meeting_title = "1:1"
    owner = user_list[5]
    participants = user_list[7:8]
    start = datetime.datetime(2021, 5, 4, 13, 30)
    end = datetime.datetime(2021, 5, 4, 14, 0)

    free_rooms = system.get_free_rooms(start, end)
    if free_rooms:
        room = free_rooms[0]
        meeting2 = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                         room=room)
        print("Created meeting: {} with id: {}".format(meeting2, meeting2.id))
    else:
        print("No more rooms from {} to {}".format(start, end))

    print("Calendar of user {}:".format(p0.name))
    pprint.pprint(system.get_user_calendar(p0))

    free_rooms = system.get_free_rooms(start, end)
    print("Free rooms from {} to {}: {}".format(start, end, free_rooms))

    """ =========================== End of meeting #3 ============================== """

    meeting_title = "Team huddle"
    owner = user_list[4]
    participants = user_list[1:7]
    start = datetime.datetime(2021, 5, 4, 14, 0)
    end = datetime.datetime(2021, 5, 4, 14, 30)

    free_rooms = system.get_free_rooms(start, end)
    if free_rooms:
        room = free_rooms[0]
        meeting2 = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                         room=room)
        print("Created meeting: {} with id: {}".format(meeting2, meeting2.id))
    else:
        print("No more rooms from {} to {}".format(start, end))

    free_rooms = system.get_free_rooms(start, end)
    print("Free rooms from {} to {}: {}".format(start, end, free_rooms))

    """ =========================== End of meeting #2 ============================== """

    # for user in system.user_list:
    #     print("Calendar of user {}:".format(user.name))
    #     pprint.pprint(system.get_user_calendar(user))
    #     print(">>>>" * 10)

    free_rooms = system.get_free_rooms(start, end)
    print("Free rooms from {} to {}: {}".format(start, end, free_rooms))

    ist = pytz.timezone("Asia/Kolkata")
    utc = pytz.timezone("UTC")

    for user in system.user_list:
        # system.print_user_calendar(user, utc)
        print(system.get_user_busy_slots(user, start.date()))
        print("=" * 80)

    # import ipdb
    # ipdb.set_trace()

    final_free_slots = system.get_free_time_slots(system.user_list, system.room_list[0], start.date())
    print("Final free slots: ")
    for free_slot in final_free_slots:
        print(free_slot)

    # """ ====================================================================================================== """
    # print("="*80)
    # print("\n"*10)
    #
    # system = CalendarSystem()
    # user_list = system.create_users(5)
    # room_list = system.create_rooms(2)
    #
    # # Create meeting #1
    # meeting_title = "Morning 0-8"
    # start = datetime.datetime(2021, 5, 4, 0, 0)
    # end = datetime.datetime(2021, 5, 4, 8, 0)
    #
    # owner = user_list[0]
    # participants = user_list[1:]
    # free_rooms = system.get_free_rooms(start, end)
    # if free_rooms:
    #     room = free_rooms[0]
    #     meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
    #                                     room=room)
    #     print("Created meeting: {} with id: {}".format(meeting, meeting.id))
    # else:
    #     print("No more rooms from {} to {}".format(start, end))
    #     return
    #
    # # Create meeting #2
    # meeting_title = "Morning 9-10"
    # start = datetime.datetime(2021, 5, 4, 9, 0)
    # end = datetime.datetime(2021, 5, 4, 10, 0)
    #
    # owner = user_list[0]
    # participants = user_list[1:3]
    # free_rooms = system.get_free_rooms(start, end)
    # if free_rooms:
    #     room = free_rooms[0]
    #     meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
    #                                     room=room)
    #     print("Created meeting: {} with id: {}".format(meeting, meeting.id))
    # else:
    #     print("No more rooms from {} to {}".format(start, end))
    #     return
    #
    # # Create meeting #3
    # meeting_title = "Morning 9:30-11"
    # start = datetime.datetime(2021, 5, 4, 9, 30)
    # end = datetime.datetime(2021, 5, 4, 11, 0)
    #
    # owner = user_list[3]
    # participants = user_list[4:]
    # free_rooms = system.get_free_rooms(start, end)
    # if free_rooms:
    #     room = free_rooms[0]
    #     meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
    #                                     room=room)
    #     print("Created meeting: {} with id: {}".format(meeting, meeting.id))
    # else:
    #     print("No more rooms from {} to {}".format(start, end))
    #     return
    #
    # # Create meeting #3
    # meeting_title = "Morning 9:30-11"
    # start = datetime.datetime(2021, 5, 4, 13, 30)
    # end = datetime.datetime(2021, 5, 4, 18, 0)
    #
    # owner = user_list[3]
    # participants = user_list[4:]
    # free_rooms = system.get_free_rooms(start, end)
    # if free_rooms:
    #     room = free_rooms[0]
    #     meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
    #                                     room=room)
    #     print("Created meeting: {} with id: {}".format(meeting, meeting.id))
    # else:
    #     print("No more rooms from {} to {}".format(start, end))
    #     return
    #
    # final_free_slots = system.get_free_time_slots(system.user_list, system.room_list[0], start.date())
    # print("Final free slots: ")
    # for free_slot in final_free_slots:
    #     print(free_slot)
    #
    # final_free_slots = system.get_free_time_slots(system.user_list, system.room_list[1], start.date())
    # print("Final free slots: ")
    # for free_slot in final_free_slots:
    #     print(free_slot)

    """ ====================================================================================================== """
    print("="*80)
    print("\n"*10)

    system = CalendarSystem()
    user_list = system.create_users(8)
    room_list = system.create_rooms(3)

    u0 = user_list[0]
    u1 = user_list[1]
    u2 = user_list[2]
    u3 = user_list[3]
    u4 = user_list[4]
    u5 = user_list[5]
    u6 = user_list[6]
    u7 = user_list[7]

    r0 = room_list[0]
    r1 = room_list[1]
    r2 = room_list[2]

    # Create meeting #1
    meeting_title = "Morning 0-8"
    start = datetime.datetime(2021, 5, 4, 0, 0)
    end = datetime.datetime(2021, 5, 4, 8, 0)

    owner = u0
    participants = user_list[1:]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                    room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    # Create meeting #2
    meeting_title = "Morning 18-24"
    start = datetime.datetime(2021, 5, 4, 18, 0)
    end = datetime.datetime(2021, 5, 5, 0, 0)

    owner = u0
    participants = user_list[1:]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants,
                                    room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    """ ------------------------------------------------------------------------------------------------- """

    meeting_title = "Meeting #1"
    start = datetime.datetime(2021, 5, 4, 8, 0)
    end = datetime.datetime(2021, 5, 4, 10, 0)

    owner = u0
    participants = [u1, u2]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    meeting_title = "Meeting #2"
    start = datetime.datetime(2021, 5, 4, 10, 0)
    end = datetime.datetime(2021, 5, 4, 12, 0)

    owner = u3
    participants = [u4]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    meeting_title = "Meeting #3"
    start = datetime.datetime(2021, 5, 4, 12, 0)
    end = datetime.datetime(2021, 5, 4, 14, 0)

    owner = u2
    participants = [u4]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    meeting_title = "Meeting #4"
    start = datetime.datetime(2021, 5, 4, 14, 0)
    end = datetime.datetime(2021, 5, 4, 16, 0)

    owner = u2
    participants = [u3]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    meeting_title = "Meeting #5"
    start = datetime.datetime(2021, 5, 4, 16, 0)
    end = datetime.datetime(2021, 5, 4, 18, 0)

    owner = u1
    participants = [u4]
    room = r0
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    meeting_title = "Meeting #6"
    owner = u5
    participants = [u5]
    room = r2

    start = datetime.datetime(2021, 5, 4, 8, 0)
    end = datetime.datetime(2021, 5, 4, 8, 30)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)
    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    start = datetime.datetime(2021, 5, 4, 9, 0)
    end = datetime.datetime(2021, 5, 4, 9, 45)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    start = datetime.datetime(2021, 5, 4, 10, 0)
    end = datetime.datetime(2021, 5, 4, 10, 15)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    start = datetime.datetime(2021, 5, 4, 11, 0)
    end = datetime.datetime(2021, 5, 4, 11, 18)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    start = datetime.datetime(2021, 5, 4, 11, 30)
    end = datetime.datetime(2021, 5, 4, 11, 50)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    start = datetime.datetime(2021, 5, 4, 13, 30)
    end = datetime.datetime(2021, 5, 4, 14, 50)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    start = datetime.datetime(2021, 5, 4, 15, 0)
    end = datetime.datetime(2021, 5, 4, 16, 30)
    meeting = system.create_meeting(owner, meeting_title, start, end, participants=participants, room=room)

    print("Created meeting: {} with id: {}".format(meeting, meeting.id))

    final_free_slots = system.get_free_time_slots(system.user_list, r0, start.date())
    print("Final free slots for r0: ")
    for free_slot in final_free_slots:
        print(free_slot)

    final_free_slots = system.get_free_time_slots([u5], r2, start.date())
    print("Final free slots for r2: ")
    for free_slot in final_free_slots:
        print(free_slot)


if __name__ == '__main__':
    main()
