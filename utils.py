def get_user_readable_datetime(timestamp):
    if timestamp.tzinfo and timestamp.tzinfo.utcoffset(timestamp):
        return timestamp.strftime("%A, %d %B %Y, %I:%M:%S %p %Z")
    else:
        return timestamp.strftime("%A, %d %B %Y, %I:%M:%S %p")


def get_user_readable_duration(timedelta):
    total_seconds = timedelta.total_seconds()

    seconds = total_seconds
    minutes = 0
    hours = 0
    days = 0

    if total_seconds >= 60:
        seconds = int(total_seconds % 60)
        minutes = int(total_seconds / 60)
        if minutes >= 60:
            hours = int(minutes / 60)
            minutes = minutes % 60

            if hours >= 24:
                days = int(hours / 24)
                hours = hours % 24

    timestamp_data = []

    if days:
        day_str = "{} day".format(days)
        if days > 1:
            day_str += "s"
        timestamp_data.append(day_str)

    if hours:
        hstr = "{} hour".format(hours)
        if hours > 1:
            hstr += "s"
        timestamp_data.append(hstr)

    if minutes:
        mstr = "{} minute".format(minutes)
        if minutes > 1:
            mstr += "s"
        timestamp_data.append(mstr)

    if seconds:
        sstr = "{} second".format(seconds)
        if seconds > 1:
            sstr += "s"
        timestamp_data.append(sstr)

    timestamp_str = ", ".join(timestamp_data)

    return timestamp_str


def filter_free_slots(free_slots, busy_slots):
    new_free_slots = []

    for free_slot in free_slots:
        for busy_slot in busy_slots:
            if busy_slot[0] >= free_slot[1]:
                break

            elif busy_slot[1] <= free_slot[0]:
                continue

            else:
                if busy_slot[0] < free_slot[0] < busy_slot[1]:
                    free_slot[0] = busy_slot[1]
                elif busy_slot[0] < free_slot[1] < busy_slot[1]:
                    free_slot[1] = busy_slot[0]
                elif busy_slot[0] >= free_slot[0] and busy_slot[1] < free_slot[1]:
                    new_free_slots.append([free_slot[0], busy_slot[0]])
                    free_slot[0] = busy_slot[1]
                elif free_slot[0] <= busy_slot[0] <= free_slot[1]:
                    new_free_slots.append([free_slot[0], busy_slot[0]])
                    free_slot[0] = busy_slot[1]
                elif free_slot[0] >= busy_slot[0] and free_slot[1] <= busy_slot[1]:
                    free_slot[0] = free_slot[1]

    new_free_slots.extend(free_slots)
    new_free_slots = list(filter(lambda e: e[0] != e[1], new_free_slots))
    new_free_slots.sort(key=lambda e: e[0])
    return new_free_slots
