import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

CHANNELS = [
    {"id":"gym_motiv",  "name":"Gym Motivation 2026",  "youtubeId":"S-zWt5mSwhc","categoria":"FITNESS",  "icono":"💪"},
    {"id":"fitness_wk", "name":"Fitness Workout Music", "youtubeId":"72qDoA3SwEs","categoria":"FITNESS",  "icono":"🏋"},
    {"id":"workout_r",  "name":"Workout Radio 24/7",    "youtubeId":"G7ksDUqUVqA","categoria":"FITNESS",  "icono":"🎵"},
    {"id":"gym_128",    "name":"Gym Music 128 BPM",     "youtubeId":"CxqCkeA63Us","categoria":"FITNESS",  "icono":"⚡"},
    {"id":"running_r",  "name":"Running Sport Radio",   "youtubeId":"YDuz4mAtyf4","categoria":"SPORT",    "icono":"🏃"},
    {"id":"maxoazo",    "name":"Max Oazo Live Radio",   "youtubeId":"OeZ88byX6E4","categoria":"SPORT",    "icono":"🎧"},
    {"id":"nature",     "name":"Nature Sounds 24/7",    "youtubeId":"-v97MKSgDHk","categoria":"WELLNESS", "icono":"🌿"},
    {"id":"meditation", "name":"Meditation 24/7",       "youtubeId":"inpok4MKVLM","categoria":"WELLNESS", "icono":"🧘"},
]

def resolve(yid):
    try:
        r = subprocess.run(["yt-dlp","--get-url","-f","b","--no-playlist",f"https://www.youtube.com/watch?v={yid}"],
            capture_output=True,text=True,timeout=30)
        lines=[l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
        return lines[0] if lines and lines[0].startswith("http") else ""
    except: return ""

ok=0
resolved=[]
for ch in CHANNELS:
    print(f"  {ch['name']}...",end=" ",flush=True)
    url=resolve(ch["youtubeId"])
    print("OK" if url else "FAIL")
    if url: ok+=1
    resolved.append({**ch,"url":url})

out={"updated":datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"ok":ok,"total":len(CHANNELS),"channels":resolved}
Path("streams.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Done: {ok}/{len(CHANNELS)}")
if ok==0: sys.exit(1)
