import os
import time
from playsound import playsound

RINGTONE_PATHS = {
    "default": "/Users/arunkumar/learning-ai/python/wind_up_alaram.mp3",
    "wind_up_alaram": "/Users/arunkumar/learning-ai/python/wind_up_alaram.mp3",
}

CLEAR = " \033[2J"
CLEAR_AND_RETURN = "\033[H"


def alarm_clock(ringtone_path=RINGTONE_PATHS["default"], alarm_clock_timer_min=1):
    """Play a sound and set an alarm clock."""
    print(
        f"Alarm clock is set for {alarm_clock_timer_min * 60} seconds"
        if alarm_clock_timer_min < 1
        else f"{alarm_clock_timer_min} minutes."
    )
    time_in_seconds = alarm_clock_timer_min * 60
    timer = 0
    while timer < time_in_seconds:
        time.sleep(1)
        remaining_time_in_minutes = timer // 60
        remaining_time_in_hours = remaining_time_in_minutes // 60
        os.system("clear")
        print(
            f"{remaining_time_in_hours:02d}:{remaining_time_in_minutes % 60:02d}:{timer:02d}"
        )
        timer += 1
    print("Alarm clock has been triggered!")
    playsound(ringtone_path)


if __name__ == "__main__":
    try:
        print("Welcome to Alarm Clock")
        ringtone_path = RINGTONE_PATHS["wind_up_alaram"]
        alarm_clock_timer = float(input("Enter the time in minutes: "))
        alarm_clock(ringtone_path, alarm_clock_timer)
    except Exception as e:
        print("Error: ", e)
