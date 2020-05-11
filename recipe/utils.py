# General use utility functions

def format_duration(m):
    """
    Takes duration in minutes 'm' (https://en.wikipedia.org/wiki/ISO_8601#Durations)
    :param m:
    :return: string in ISO8601 duration format
    """
    hrs = m // 60
    mins = m % 60
    return f"PT{str(hrs) if hrs else ''}H{str(mins) if mins else ''}M"