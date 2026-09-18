"""Import FFDec exports of Suzy's preserved site; originals are never modified.

Usage: uv run --with pillow scripts/import-joe-creations.py EXPORT_DIRECTORY
EXPORT_DIRECTORY contains <movie>/frames/3.svg, movie.xml, scripts/, the
extracted child movie images, geometry.json, and logo/slogan sprite exports.
See docs/JOE_RESTORATION.md for the extraction procedure and source limits.
"""
import base64
import io
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from PIL import Image

SOURCE = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'src/images/joe-creations'
ASSETS.mkdir(parents=True, exist_ok=True)
DATA = ROOT / 'src/_data'
DATA.mkdir(parents=True, exist_ok=True)
GEOMETRY = json.loads((SOURCE.parent / 'geometry.json').read_text())
PAGES = {
    'indexfla': ('index', 'Joseph Neyer Creations'),
    'atkinsfla': ('atreno', 'Atkins renovation'),
    'beeryfla': ('brreno', 'Beery renovation'),
    'bialesfla': ('bldesign', 'Biales design and build'),
    'drstudiofla': ('drstudio', 'Drumming studio'),
    'elliotfla': ('elreno', 'Elliot renovation'),
    'neyerfla': ('nrreno', 'Neyer renovation'),
    'treehousefla': ('trhouse', 'Treehouse'),
}
TITLES = {slug: title for slug, title in PAGES.values()}
TITLES['spporch'] = 'Porch'

def optimize_svg(source, name, remove_character=None):
    text = source.read_text()
    if remove_character:
        text = re.sub(r'<use\b(?=[^>]*ffdec:characterId="'+remove_character+r'")[^>]*/>', '', text)
    # Keep the original vector lettering, colors, masks and composition.
    # Downsample only the photographs embedded inside small oval thumbnails.
    def compact(match):
        image = Image.open(io.BytesIO(base64.b64decode(match[1])))
        image.thumbnail((640, 640))
        output = io.BytesIO()
        image.convert('RGB').save(output, 'JPEG', quality=88, optimize=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(output.getvalue()).decode()
    text = re.sub(r'data:image/jpeg;base64,([A-Za-z0-9+/=\s]+?)(?=["\'])', compact, text)
    width = re.search(r'\bwidth="([\d.]+)px"', text)[1]
    height = re.search(r'\bheight="([\d.]+)px"', text)[1]
    text = text.replace('<svg ', f'<svg viewBox="0 0 {width} {height}" ', 1)
    (ASSETS / name).write_text(text)
    return '/images/joe-creations/' + name

def image_for(movie):
    directory = SOURCE / Path(movie).with_suffix('')
    candidates = list(directory.glob('*.jpg')) + list(directory.glob('*.png'))
    if not candidates:
        return None
    source = max(candidates, key=lambda p: p.stat().st_size)
    name = movie.replace('/', '-').replace('.swf', '.jpg')
    image = Image.open(source)
    image.thumbnail((1600, 1200))
    image.convert('RGB').save(ASSETS / name, 'JPEG', quality=92, optimize=True)
    return '/images/joe-creations/' + name

def style(box):
    return ';'.join(f'{key}:{box[field]/denominator*100:.5f}%'
                    for key,field,denominator in [('left','x',2200),('top','y',1000),
                                                  ('width','width',2200),('height','height',1000)])

pages = []
for movie, (slug,title) in PAGES.items():
    export = SOURCE / movie
    xml = ET.parse(export / 'movie.xml').getroot()
    names = {tag.get('name'): tag.get('characterId') for tag in xml.find('tags')
             if tag.get('name') and tag.get('characterId')}
    action = (export / 'scripts/frame_3/DoAction.as').read_text()
    buttons = []
    for box in GEOMETRY[movie]:
        name = box['id']
        if not name or name not in names or box['width'] == 0:
            continue
        script_dir = export / 'scripts' / ('DefineButton2_' + names[name])
        scripts = '\n'.join(p.read_text() for p in script_dir.glob('*.as'))
        target = re.search(r'getURL\("([^"]+)"', scripts)
        timeline_photo = re.search(re.escape(name) + r'\.onRollOver = function\(\).*?mcl.loadClip\("([^"]+)"', action, re.S)
        candidates = re.findall(r'loadMovie(?:Num)?\("([^"]+)"', scripts)
        photo = timeline_photo[1] if timeline_photo else next((p for p in candidates if (SOURCE / Path(p).with_suffix('')).exists()), candidates[0] if candidates else None)
        if name == 'home' or (target and target[1] == 'index.html'):
            continue
        if not photo:
            continue
        target_slug = target[1].replace('.html', '') if target else None
        image = image_for(photo)
        # The porch's linked files did not survive in this shared folder.
        # The original homepage thumbnail is the only verified visual source.
        if not image and target_slug == 'spporch':
            image = '/images/joe-creations/porch-surviving-thumbnail.jpg'
        buttons.append({'id': name, 'label': TITLES.get(target_slug, title),
                        'target': target_slug, 'photo': image, 'source': photo,
                        'style': style(box)})
    if slug != 'index':
        buttons.sort(key=lambda b:int(re.search(r'(\d+)\.swf$',b['source'])[1]))
        for n, button in enumerate(buttons):
            button['label'] = f'{title} — photograph {n+1}'
    initial = re.search(r'mcl.loadClip\("([^"]+)"',action)
    holder = next((b for b in GEOMETRY[movie] if b['id']=='holder'),None)
    # Home holder is a masked sprite with no named <use> in the exported frame.
    if not holder:
        holder = {'x':895,'y':216,'width':737,'height':554}
    animation = next((p.parent.parent.name.split('_')[-1] for p in (export/'scripts').glob('DefineSprite_*/frame_55/DoAction.as')), None)
    pages.append({'slug':slug,'title':title,'home':slug=='index',
                  'background':optimize_svg(export/'frames/3.svg', movie+'.svg', animation),
                  'buttons':buttons,'initial':image_for(initial[1]) if initial else None,
                  'photoStyle':style(holder), 'source':movie+'.swf'})

# Recover the porch thumbnail from the original home movie's image objects.
# Its source ID is identified by the original masked image's location.
porch = SOURCE / 'home/images/43.jpg'
if porch.exists():
    image = Image.open(porch)
    image.thumbnail((1600,1200))
    image.convert('RGB').save(ASSETS/'porch-surviving-thumbnail.jpg',quality=92)

optimize_svg(SOURCE/'slogan/DefineSprite_61/49.svg','slogan.svg')
heading = ET.parse(ASSETS/'slogan.svg').getroot()
heading.set('viewBox','26.1 0.25 481.3952 86.761')
heading.set('width','481.3952')
heading.set('height','86.761')
(ASSETS/'slogan.svg').write_bytes(ET.tostring(heading))
optimize_svg(SOURCE/'gallery-slogan/DefineSprite_61/55.svg','gallery-slogan.svg')
# Crop the final lettering to its visible bounds, excluding the morph's earlier
# curved states (FFDec includes those in the default exported sprite viewport).
heading = ET.parse(ASSETS/'gallery-slogan.svg').getroot()
heading.set('viewBox','33.75 36.1 495.7 34.1')
heading.set('width','495.7')
heading.set('height','34.1')
(ASSETS/'gallery-slogan.svg').write_bytes(ET.tostring(heading))
# The gold glow belongs to the logo's placement in the movie, not its button.
# Preserve that placement and its SVG filter when extracting a standalone mark.
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
logo = ET.parse(ASSETS/'indexfla.svg').getroot()
group = logo.find('{http://www.w3.org/2000/svg}g')
for element in list(group):
    if element.tag.endswith('}use') and element.get('{https://www.free-decompiler.com/flash}characterId') != '6':
        group.remove(element)
logo.set('viewBox','65 25 345 260')
logo.set('width','345')
logo.set('height','260')
(ASSETS/'logo.svg').write_bytes(ET.tostring(logo))
(DATA/'joeCreations.json').write_text(json.dumps(pages,indent=2)+'\n')
print(f'Imported {len(pages)} screens and {sum(len(p["buttons"]) for p in pages)} interactive thumbnails.')
