# Chris Public OSBC Scripts
# 

|                                 |                           |                               |
|---------------------------------|---------------------------|-------------------------------|
| [Overview](#overview) | [Chris BowlFiller](#chris-bowl-filler) | [Chris DhideCrafterAlcher](#chris-dhide-crafter-alcher) |







## Overview
This is (for now) based on willowdads bot classes, so you'll need to configure and set up that first. You can read how to do that here:
https://github.com/WillowsDad/WillowsDad-Scripts




### Chris Bowl Filler
Super simple script which runs from the falador west bank to the waterpump and fills bowls. It fills a bit more than 2000 bowls an hour. The script isn't perfect and at rare occations might decide to run out of falador.
#### Features and Setup
- Edit `/src/model/osrs/__init__.py` and add `from .WillowsDad.ChrisBowlFiller import OSRSChrisBowlFiller` at the end of the file.
- Put the pictures into `\src\model\osrs\WillowsDad\WillowsDad_images`
- Put the `ChrisBowlFiller.py` file into `\src\model\osrs\WillowsDad`
- Banks should be tagged yellow
- Waterpump should be tagge pink
- Bank deposit settings should be set to "All"
- Angle/zoom out the camera so both the Bank and the Waterpump can be seen on the same screen.



### Chris Dhide Crafter Alcher
A feature rich script which crafts dragonhide bodies and alches them. Xp rates are 170-175k/h combined xp using the bank, and 175-180k/h when unnoting. Make sure your inventory contains thread, at least one coin and a needle.
#### Features
- Can craft straight from the bank. Requires a staff of fire or tome of fire and nature runes in the inventory.
- Can craft using notes (by using on the bank) for slightly faster xp rates. This requires you to use Bryophyta's staff and a Tome of fire.
- Works on all banks and bankchests.
- Requires the use of F keys and ESC. You can change this manually if you want.
- DOES NOT contain a function to automatically charge the staff with new nature runes.

#### Setup
- Edit `/src/model/osrs/__init__.py` and add `from .WillowsDad.ChrisDhideCraftAlcher import OSRSChrisDhideCraftAlcher` at the end of the file.
- Put the pictures into `\src\model\osrs\WillowsDad\WillowsDad_images`
- Put the `ChrisDhideCraftAlcher.py` file into `\src\model\osrs\WillowsDad`
- Banks should be tagged yellow
- Bank deposit settings should be set to "All" if you have 24 spaces in your inventory. Otherwise any value dividable in 3.
