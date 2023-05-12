# Chris Public OSBC Scripts
# 

|                                 |                           |                               |
|---------------------------------|---------------------------|-------------------------------|
| [Overview](#overview) | [Chris BowlFiller](#chris-bowl-filler) |  |







## Overview
This is (for now) based on willowdads bot classes, so you'll need to configure and set up that first. You can read how to do that here:
https://github.com/WillowsDad/WillowsDad-Scripts




### Chris Bowl Filler
Super simple script which runs from the falador west bank to the waterpump and fills bowls. It fills a bit more than 2000 bowls an hour. The script isn't perfect and at rare occations might decide to run out of falador.
#### Features and Setup
- Edit /src/model/osrs/__init__.py and add "from .WillowsDad.ChrisBowlFiller import OSRSChrisBowlFiller" at the end of the file.
- Put the pictures into \src\model\osrs\WillowsDad\WillowsDad_images
- Put the ChrisBowlFiller.py file into \src\model\osrs\WillowsDad
- Banks should be tagged yellow
- Trees should be tagge pink
- Bank deposit settings should be set to "All"
