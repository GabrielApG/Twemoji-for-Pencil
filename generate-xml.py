from lxml import etree
from pathlib import Path
import cairosvg
import os
import shutil
import re
import json

sprite_files = sorted(list(Path('./twemoji/svg/').glob('*.svg')), key=lambda file: file.as_posix())
files_element = etree.Element("files")

with open('emoji.json') as data_file:
	emoji_map = json.load(data_file)

# set up the output dir
out = Path('gen/')
icons_out = Path(out, 'icons/')

if out.exists and out.is_dir():
	shutil.rmtree(str(out))

icons_out.mkdir(parents=True)

for f in sprite_files:
	element = etree.SubElement(files_element, 'file')
	element.text = f.as_posix()
	element.set('id', f.stem)

	emoji_key = f.stem

	if emoji_key in emoji_map:
		emoji_name = (emoji_map[emoji_key]).title()
	else:
		emoji_name = f.stem

	element.set('name', emoji_name)

	icon_name = f.stem + '.png'
	element.set('icon', icons_out.relative_to(out).joinpath(icon_name).as_posix()) # Pencil uses Unix-style paths for icons

	with open(os.path.join(str(icons_out), icon_name),'wb+') as icon_out:
		thumb = cairosvg.svg2png(file_obj=str(f), write_to=icon_out)

stylesheet = etree.parse('stylesheet.xsl')
transform = etree.XSLT(stylesheet)

result = transform(files_element)

result.write(os.path.join(str(out), 'Definition.xml'), pretty_print=True)
