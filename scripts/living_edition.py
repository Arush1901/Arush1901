"""Render Folio's contribution landscape using only Python's standard library."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'data-level' in attrs:
            day = date.fromisoformat(attrs['data-date']).isoformat()
            level = int(attrs['data-level'])
            if not 0 <= level <= 4:
                raise ValueError('Invalid contribution intensity')
            self.days[day] = level


def calendar_days(html, as_of):
    """Ignore GitHub's future cells; reject incomplete or changed markup."""
    parser = Calendar()
    parser.feed(html)
    first = date(as_of.year, 1, 1)
    days = {day: level for day, level in parser.days.items()
            if first.isoformat() <= day <= as_of.isoformat()}
    if len(days) != (as_of-first).days+1:
        raise ValueError('Incomplete contribution calendar; retaining the previous artwork')
    return dict(sorted(days.items()))


def group_weeks(days):
    first, last = date.fromisoformat(min(days)), date.fromisoformat(max(days))
    start = first-timedelta(days=(first.weekday()+1) % 7)
    weeks = []
    while start <= last:
        levels = [days.get((start+timedelta(days=i)).isoformat(), 0) for i in range(7)]
        weeks.append({'start': start.isoformat(), 'levels': levels,
                      'intensity': round(sum(levels)/28, 5),
                      'activeDays': sum(level > 0 for level in levels)})
        start += timedelta(days=7)
    return weeks


def fetch_snapshot(username):
    if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', username):
        raise ValueError('Invalid GitHub username')
    today = datetime.now(timezone.utc).date()
    source = (f'https://github.com/users/{username}/contributions'
              f'?from={today.year}-01-01&to={today.isoformat()}')
    request = Request(source, headers={'User-Agent': 'Folio-Living-Edition', 'Accept': 'text/html'})
    with urlopen(request, timeout=45) as response:
        html = response.read(3_000_001)
    if len(html) > 3_000_000:
        raise ValueError('Unexpected calendar response size')
    days = calendar_days(html.decode('utf-8'), today)
    return {'username': username, 'source': source, 'captured': today.isoformat(),
            'first': min(days), 'last': max(days), 'days': days, 'weeks': group_weeks(days)}


def bell(x, center, width):
    return math.exp(-((x-center)/width)**2)


def strand_path(index, weeks, maximum):
    week = weeks[index]
    v = index/max(len(weeks)-1, 1)
    activity = math.sqrt(week['intensity']/maximum)
    points = []
    for j in range(201):
        u = j/200
        x = 61+654*u+v*(42*(1-u)-12*u)+14*math.sin(math.pi*u)*math.sin(math.pi*v)
        y = 175+73*v
        y -= (109-25*v)*bell(u, .265+.11*v, .19)
        y += (22+22*v)*bell(u, .515+.035*v, .105)
        y -= (87+6*v)*bell(u, .765-.075*v, .17)
        y += 13*math.sin(math.pi*v)*math.sin(2.5*math.pi*u+.6)
        envelope = math.sin(math.pi*u)**1.3
        y += activity*5.2*envelope*math.sin(2*math.pi*u+.8*v)
        impression = sum((level/4)*bell(u, (day+.5)/7, .115)
                         for day, level in enumerate(week['levels']))
        y -= 2.8*impression*envelope
        points.append(('M' if j == 0 else 'L')+f'{x:.2f},{y:.2f}')
    return ' '.join(points)


def render(snapshot, theme='light', mobile=False, still=False):
    weeks = group_weeks(snapshot['days'])
    maximum = max(w['intensity'] for w in weeks) or 1
    uid = 'living-'+('mobile' if mobile else 'desktop')
    ink, rule, accent, paper, text = '#55544f', '#d8d2c6', '#a0523e', '#faf8f3', '#292d32'
    if theme == 'dark':
        ink, rule, accent, paper, text = '#c6c5be', '#3b3d3b', '#d39a7e', '#171b1e', '#e7e8e7'
    width, height, offset, scale = (420, 218, 45, 420/780) if mobile else (780, 379, 59, 1)
    css = f'''
#{uid} .frame{{fill:{paper};stroke:{rule};stroke-width:.8}}
#{uid} .lines{{animation:presence 22s linear infinite}}
#{uid} .strand{{fill:none;stroke:{ink};stroke-width:.72;stroke-linecap:round;vector-effect:non-scaling-stroke;stroke-dasharray:1;stroke-dashoffset:0}}
#{uid} .warm{{stroke:{accent}}}
@keyframes presence{{0%{{opacity:0}}3%,85%{{opacity:1}}96%,100%{{opacity:0}}}}
'''
    paths = []
    seam = round((len(weeks)-1)*24/42)
    for i, week in enumerate(weeks):
        start = 1.5+15*i/max(len(weeks)-1, 1)
        css += f'@keyframes strand-{i}{{0%,{start:.3f}%{{stroke-dashoffset:1}}{start+25:.3f}%,100%{{stroke-dashoffset:0}}}}\n'
        alpha = .28+.40*math.sqrt(week['intensity']/maximum)
        warm = ' warm' if abs(i-seam) <= 1 else ''
        paths.append(f'<path class="strand{warm}" data-week="{week["start"]}" d="{strand_path(i, weeks, maximum)}" pathLength="1" opacity="{alpha:.3f}" style="animation:strand-{i} 22s cubic-bezier(.35,.05,.25,1) infinite"/>')
    if mobile:
        css += f'#{uid} .strand:nth-child(even){{display:none}}\n'
    css += f'''@media(prefers-reduced-motion:reduce){{
#{uid} .lines,#{uid} .strand{{animation:none!important}}
#{uid} .lines{{opacity:1}}#{uid} .strand{{stroke-dashoffset:0}}
}}'''
    if still:
        css += f'''#{uid} .lines,#{uid} .strand{{animation:none!important}}
#{uid} .lines{{opacity:1}}#{uid} .strand{{stroke-dashoffset:0}}'''
    description = (f'A flowing landscape shaped by {len(weeks)} weeks of public GitHub activity, '
                   f'{snapshot["first"]} to {snapshot["last"]}. Each week contributes a strand; '
                   'activity changes its depth and ink. The folded surface is an artistic composition.')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" id="{uid}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{uid}-title {uid}-desc">
<title id="{uid}-title">A little work, every day.</title><desc id="{uid}-desc">{escape(description)}</desc>
<style>{css}</style>
<text x="0" y="{29 if mobile else 30}" fill="{text}" font-family="Georgia,'Times New Roman',serif" font-size="{28 if mobile else 29}" letter-spacing="-.6">A little work, every day.</text>
<g transform="translate(0 {offset}) scale({scale})"><rect x="1" y="1" width="778" height="317" class="frame"/><g class="lines">{''.join(paths)}</g></g>
</svg>'''
    ET.fromstring(svg)
    return svg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Fetch the public year-to-date calendar')
    parser.add_argument('--username', default='Arush1901')
    args = parser.parse_args()
    data_file = ROOT/'data/contributions.json'
    snapshot = fetch_snapshot(args.username) if args.refresh else json.loads(data_file.read_text(encoding='utf-8'))
    # Generate and validate every variant before replacing any existing artwork.
    assets = {f'living-edition{"-mobile" if mobile else ""}-{theme}{"-still" if still else ""}.svg': render(snapshot, theme, mobile, still)
              for theme in ['light', 'dark'] for mobile in [False, True] for still in [False, True]}
    (ROOT/'assets').mkdir(exist_ok=True)
    data_file.parent.mkdir(exist_ok=True)
    for name, svg in assets.items():
        (ROOT/'assets'/name).write_text(svg, encoding='utf-8')
    data_file.write_text(json.dumps(snapshot, indent=2)+'\n', encoding='utf-8')
    print(f'Generated 8 landscape SVGs from {len(group_weeks(snapshot["days"]))} calendar weeks.')


if __name__ == '__main__':
    main()
