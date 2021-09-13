import requests
from ruamel.yaml import YAML
import dateutil.parser
import dateutil.tz
from datetime import timedelta
from parse import parse
from pprint import pprint
from markdown import Markdown
import bleach
from os import environ
import os, os.path

PRETALX_TOKEN = environ["PRETALX_TOKEN"]
AEST = dateutil.tz.gettz("Australia/Melbourne")

yaml = YAML()
md = Markdown()


def paginate(url):
    next_url = url
    while next_url:
        res = requests.get(
            next_url,
            headers={"Authorization": f"Token {PRETALX_TOKEN}"},
        )
        res.raise_for_status()
        data = res.json()
        next_url = data["next"]
        yield from data["results"]


def parse_markdown(text):
    html = md.convert(text)
    return bleach.clean(
        html,
        tags=(
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "p",
            "h2",
            "h3",
            "s",
            "del",
            "ins",
        ),
    )


rooms = {
    "Backup Speakers": 0,
    "Curlyboi Theatre": 1,
    "Platypus Hall": 2,
    "Science, Data & Analytics": 1,
    "DevOops": 2, 
    "Education": 3,
    "Snakeoil Academy (Security & Privacy)": 4
}

tracks = {
    "DevOops": "devoops",
    "Science, Data, and Analytics": "science",
    "Education": "education",
    "Snakeoil Academy (Security & Privacy)": "snakeoil",
    "Main Conference": None,
}

answers = {
    "Presentation Format": 853,
    "Content Warning": 854, 
    "Pronouns": 856
}

format_answer = {
    1062: "L", # live
    1063: "P", # prerecord
}

seen_speakers = set()

yt_resp = requests.get(
    "https://portal.nextdayvideo.com.au/main/C/pyconau/S/pyconau_2021.json"
)
yt_resp.raise_for_status()
youtube_slugs = {
    x["conf_key"]: x["host_url"].rsplit("/", 1)[1]
    for x in yt_resp.json()
    if x["host_url"] is not None
}

for entry in os.listdir("data/Session/"):
    os.unlink(f"data/Session/{entry}")

for session in paginate("https://pretalx.com/api/events/pycon-au-2021/talks/"):

    # Do not schedule backups
    # TODO manually add backups if they are unscheduled after the event.
    if rooms[session["slot"]["room"]["en"]] == 0: 
        print("not scheduling backup")
        continue

    speakers = [x["code"] for x in session["speakers"]]
    seen_speakers.update(speakers)
    with open(f'data/Session/{session["code"]}.yml', "w") as f:
        start = dateutil.parser.isoparse(session["slot"]["start"]).astimezone(AEST)
        end = dateutil.parser.isoparse(session["slot"]["end"]).astimezone(AEST)
        type_answer_id = format_answer[next(
                x["options"][0]["id"] for x in session["answers"] if x["question"]["id"] == answers["Presentation Format"]
            )]
        try:
            cw = next(
                x["answer"] for x in session["answers"] if x["question"]["id"] == answers["Content Warning"]
            )
        except (StopIteration, IndexError):
            cw = None
        yaml.dump(
            {
                "title": session["title"],
                "start": start,
                "end": end,
                "room": rooms[session["slot"]["room"]["en"]],
                "track": tracks[session["track"]["en"]],
                "type": type_answer_id,
                "abstract": parse_markdown(session["abstract"]),
                "description": parse_markdown(session["description"]),
                "code": session["code"],
                "speakers": speakers,
                "cw": parse_markdown(cw) if cw is not None else None,
                "youtube_slug": youtube_slugs.get(session["code"]),
            },
            f,
        )

from PIL import Image
from io import BytesIO

with open("assets/people/_etags.yml") as f:
    etags = yaml.load(f)

# etags none? ensure empty
if not etags: 
    etags = {}

for speaker in paginate("https://pretalx.com/api/events/pycon-au-2021/speakers/"):
    if speaker["code"] not in seen_speakers:
        continue
    has_pic = False
    try:
        if speaker["avatar"] is not None:
            etag = etags.get(speaker["code"], None)
            avatar_resp = requests.get(
                speaker["avatar"],
                headers={"If-None-Match": etag} if etag is not None else {},
            )
            if avatar_resp.status_code == 304:
                print("ETag match")
                continue
            avatar_resp.raise_for_status()
            if "ETag" in avatar_resp.headers:
                etags[speaker["code"]] = avatar_resp.headers["ETag"]
            im = Image.open(BytesIO(avatar_resp.content))
            im = im.convert("RGB")
            im.thumbnail((128, 128))
            im.save(f'assets/people/{speaker["code"]}.jpg')
            has_pic = True
    except Exception as e:
        print(speaker["code"], speaker["avatar"], e)
    with open(f'data/Person/{speaker["code"]}.yml', "w") as f:
        yaml.dump(
            {
                "name": speaker["name"],
                "pronouns": next(
                    (
                        x["answer"]
                        for x in speaker["answers"]
                        if x["question"]["id"] == answers["Pronouns"]
                    ),
                    None,
                ),
                "bio": parse_markdown(speaker["biography"] or ""),
                "has_pic": has_pic,
            },
            f,
        )

with open("assets/people/_etags.yml", "w") as f:
    yaml.dump(etags, f)
