import webbrowser, json, sys
from datetime import datetime, timedelta

def main(argv):
    if (len(argv) < 2):
        print("Usage: " + argv[0] + " filepath <if_summertime> <possible_delay>")
        return
    if (len(argv) < 3):
        summertime = False
    else:
        summertime = argv[2] == "True" or argv[2] == "true"
    if (len(argv) < 4):
        delay_possible = timedelta(minutes=0)
    else:
        delay_possible = timedelta(minutes=int(argv[3]))
    today = datetime.today() - delay_possible
    if summertime:
        today += timedelta(hours=1)
    lessons_file = open(argv[1], "r", encoding="utf-8")
    if not lessons_file:
        print("failed to open file " + argv[1])
        return
    lessons = json.loads(lessons_file.read())
    lessons_file.close()
    weekday = today.weekday()
    week_number = today.strftime("%V")
    if int(week_number) % 2 == 1:
        week_parity = "even"
    else:
        week_parity = "odd"
    time_hour = int(today.time().strftime("%H"))
    time_minute = int(today.time().strftime("%M"))
    lessons_today = lessons[str(weekday)]
    closest_lesson = {"name": "placeholder", "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "time_hour": 24, "time_minute": 60}
    for lesson in lessons_today:
        if not lesson[week_parity]:
            continue
        if time_hour > lesson["time_hour"]:
            continue
        if time_hour == lesson["time_hour"] and time_minute > lesson["time_minute"]:
            continue
        if lesson["time_hour"] < closest_lesson["time_hour"]:
            closest_lesson = lesson
        if lesson["time_hour"] == closest_lesson["time_hour"] and lesson["time_minute"] < closest_lesson["time_minute"]:
            closest_lesson = lesson
    print("Dołączanie do " + closest_lesson["name"])
    webbrowser.open(closest_lesson["link"], new=2)

if __name__ == '__main__':
    main(sys.argv)
