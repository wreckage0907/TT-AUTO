from flask import Flask, render_template, request, send_file
import json
import re

app = Flask(__name__)
def read_raw_data(file_path):
    with open(file_path, "r") as f:
        return f.read()

def parse_course_data(raw_data):
    b = raw_data.split("Total Number Of Credits")
    c = b[0]
    d = b[1].partition("\n")[-1]

    dic = {}
    k = 0
    for i in c.split("\n"):
        try:
            if int(i):
                k += 1
                dic[int(k)] = []
        except:
            if k > 0:
                if i not in ["", "- Manual", "Registered and Approved", "General (Semester)"] and not re.match(r"\d{2}-\w{3}-\d{4} \d{2}:\d{2}", i) and not re.match(r"\d{2}-\w{3}-\d{4}", i):
                    if " - " in i:
                        dic[k].append(i.strip().split(" - ")[0])
                        dic[k].append(i.strip().split(" - ")[-1])
                    else:
                        dic[k].append(i.strip().split(" -")[0])

    for i in dic:
        dic[i] = list(map(lambda x: x.replace('( Soft Skill )', 'TH'), dic[i]))
        dic[i] = list(map(lambda x: x.replace('( Theory Only )', 'TH'), dic[i]))
        dic[i] = list(map(lambda x: x.replace('( Lab Only )', 'LO'), dic[i]))
        dic[i] = list(map(lambda x: x.replace('( Embedded Theory )', 'ETH'), dic[i]))
        dic[i] = list(map(lambda x: x.replace('( Embedded Lab )', 'ELA'), dic[i]))
        dic[i] = list(filter(lambda x: x not in ["", "- Manual", "Registered and Approved", "General (Semester)","Weekend Intra (Semester)","Registered, Invoice Generated, Fees Paid and Approved"], dic[i]))

    return dic, d

def read_timings(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def parse_timings_data(d):
    d = d.replace("-SS-", "-TH-")
    d = d.split("\n")[4:]

    MON, TUE, WED, THU, FRI, SAT, SUN = d[:2], d[2:4], d[4:6], d[6:8], d[8:10], d[10:12], d[12:14]

    return MON, TUE, WED, THU, FRI, SAT, SUN


def create_timetable(day_data, dic, timings):
    timings["ETH"]=timings["TH"]
    timings["ELA"]=timings["LO"]
    timetable = []
    for i in day_data:
        tt = []
        for j in i:
            if "-" in j:
                try:
                    for _ in dic:
                        if j.split("-")[2] in dic[_] and j.split("-")[1] in dic[_]:
                            title = dic[_][1]
                            professor = f"{dic[_][-2]}"
                    tt.append({
                        "Title": title,
                        "Location": "-".join(j.split("-")[3:5]),
                        "Description": f"{professor} ({j.split('-')[1]})",
                        "Start": timings[j.split("-")[2]][str(i.index(j) + 1)]["start"],
                        "End": timings[j.split("-")[2]][str(i.index(j) + 1)]["end"]
                    })
                except:
                    pass
        timetable.append(tt)
    return timetable




if __name__ == "__main__":
    raw_data = read_raw_data("vtop.txt")
    course_data, timings_data = parse_course_data(raw_data)
    
    timings = read_timings("timings.json")
    MON, TUE, WED, THU, FRI, SAT, SUN = parse_timings_data(timings_data)
    
    days = [MON, TUE, WED, THU, FRI, SAT, SUN]
    timetable = {}

    for day_name, day_data in zip(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"], days):
        if(day_data):
            day_data[0] = day_data[0].partition("THEORY\t")[-1].split("\t")
            day_data[1] = day_data[1].partition("LAB\t")[-1].split("\t")
            day_data[0].remove("Lunch")
            day_data[1].remove("Lunch")

        timetable[day_name] = create_timetable(day_data, course_data, timings)

    with open("wwi.json", "w") as json_file:
        json.dump(timetable, json_file, indent=2)


