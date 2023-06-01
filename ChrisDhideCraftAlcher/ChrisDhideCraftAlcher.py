import time
from model.osrs.WillowsDad.WillowsDad_bot import WillowsDadBot

import utilities.api.item_ids as ids
import utilities.color as clr
from utilities.geometry import RuneLiteObject
import utilities.api.animation_ids as animation
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
import pyautogui as pag
import utilities.imagesearch as imsearch
import random
import pytweening


class OSRSChrisDhideCraftAlcher(WillowsDadBot):
    def __init__(self):
        bot_title = "Chris Dhide crafter & alcher"
        description = "Crafts Dhide bodies and alches it"
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = 60
        self.take_breaks = True
        self.afk_train = True
        self.delay_min =0.37
        self.delay_max = .67
        self.leather_type = ids.GREEN_DRAGON_LEATHER
        self.unnoteid = self.leather_type + 1
        self.bank_picture = "Green_dragon_leather_bank.png"
        self.toalch = ids.GREEN_DHIDE_BODY
        self.menufinder = False
        self.unnoting_setting = False
        self.unnotemenufinder = False

    def create_options(self):
        """
        Use the OptionsBuilder to define the options for the bot. For each function call below,
        we define the type of option we want to create, its key, a label for the option that the user will
        see, and the possible values the user can select. The key is used in the save_options function to
        unpack the dictionary of options after the user has selected them.
        """
        super().create_options()   # This line is required to ensure that the parent class's options are created.
        self.options_builder.add_checkbox_option("unnoting_setting", "Unnote instead of banking?", [" "])
        self.options_builder.add_dropdown_option("dhide_type", "What kind of leather?", ["Green Dragonhide", "Blue Dragonhide", "Red Dragonhide", "Black Dragonhide"])
        


    def save_options(self, options: dict):
        """
        For each option in the dictionary, if it is an expected option, save the value as a property of the bot.
        If any unexpected options are found, log a warning. If an option is missing, set the options_set flag to
        False.
        """
        super().save_options(options)  # This line is required to ensure that the parent class's options are saved.

        for option in options:
            if option == "dhide_type":
                if options[option] == "Green Dragonhide":
                    self.leather_type = ids.GREEN_DRAGON_LEATHER
                    self.bank_picture = "Green_dragon_leather_bank.png"
                    self.toalch = ids.GREEN_DHIDE_BODY
                    self.unnoteid = self.leather_type + 1

                elif options[option] == "Blue Dragonhide":
                    self.leather_type = ids.BLUE_DRAGON_LEATHER
                    self.bank_picture = "Blue_dragon_leather_bank.png"
                    self.toalch = ids.BLUE_DHIDE_BODY
                    self.unnoteid = self.leather_type + 1

                elif options[option] == "Red Dragonhide":
                    self.leather_type = ids.RED_DRAGON_LEATHER
                    self.bank_picture = "Red_dragon_leather_bank.png"
                    self.toalch = ids.RED_DHIDE_BODY
                    self.unnoteid = self.leather_type + 1

                elif options[option] == "Black Dragonhide":
                    self.leather_type = ids.BLACK_DRAGON_LEATHER
                    self.bank_picture = "Black_dragon_leather_bank.png"
                    self.toalch = ids.BLACK_DHIDE_BODY
                    self.unnoteid = self.leather_type + 1


            elif option == "unnoting_setting":
                self.unnoting_setting = options[option] != []
                    

            else:
                self.log_msg(f"Unexpected option: {option}")

        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{'' if self.take_breaks else ' not'} take breaks.")
        self.log_msg(f"Bot will{'' if self.afk_train else ' not'} train like you're afk on another tab.")
        self.log_msg(f"Bot will craft {options['dhide_type']} bodies.")
        self.log_msg("Options set successfully.")
        self.options_set = True

    def main_loop(self):
        """
        Main bot loop. We call setup() to set up the bot, then loop until the end time is reached.
        """
        # Setup APIs
        # api_m = MorgHTTPSocket()
        # api_s = StatusSocket()
        self.setup()
        
        # Main loop
        while time.time() - self.start_time < self.end_time:

            runtime = int(time.time() - self.start_time)
            minutes_since_last_break = int((time.time() - self.last_break) / 60)
            seconds = int(time.time() - self.last_break) % 60
            percentage = (self.multiplier * .01)  # this is the percentage chance of a break
            deposit_slots = self.api_m.get_first_occurrence(self.deposit_ids)
            self.roll_chance_passed = False

            try:
                # Inventory finished, deposit and withdraw
                if self.api_m.get_first_occurrence(ids.THREAD) == -1:
                    self.log_msg("Out of thread, stopping.")
                    self.stop()

                if self.api_m.get_first_occurrence(ids.NEEDLE) == -1:
                    self.log_msg("Withdraw a needle ffs, stopping.")
                    self.stop()

                if self.api_m.get_first_occurrence(self.toalch) == -1 and self.api_m.get_first_occurrence(self.leather_type) == -1:
                    if not self.is_runelite_focused():
                        pag.hotkey("alt", "tab")
                        time.sleep(self.random_sleep_length())
                    if self.unnoting_setting:
                        self.unnotingonbank()
                    else:
                        self.log_msg("Open the bank")
                        self.open_bank()
                        time.sleep(self.random_sleep_length())
                        #self.check_deposit_all()
                        self.log_msg("Check and withdraw supplies")
                        supplies_left = self.withdraw_items(self.withdraw_paths[0])
                        if not supplies_left:
                            self.log_msg("Out of supplies, stopping.")
                            self.stop()
                        self.log_msg("Close bank")
                        pag.press("esc")

                if self.api_m.get_first_occurrence(self.leather_type) != -1 and self.api_m.get_first_occurrence(self.toalch) == -1:
                    self.crafting_part()

                if self.api_m.get_first_occurrence(self.leather_type) == -1 and self.api_m.get_first_occurrence(self.toalch) != -1:
                    self.log_msg("Starting to high alch")
                    if not self.is_runelite_focused():
                        pag.hotkey("alt", "tab")
                        time.sleep(self.random_sleep_length())
                    pag.press("f6")
                    self.alcher()
                    pag.press("esc")
                    time.sleep(self.random_sleep_length())


            except Exception as e:
                self.log_msg(f"Exception: {e}")
                self.loop_count += 1
                if self.loop_count > 5:
                    self.log_msg("Too many exceptions, stopping.")
                    self.log_msg(f"Last exception: {e}")
                    self.stop()
                continue

            # -- End bot actions --
            self.loop_count = 0
            if self.take_breaks:
                self.check_break(runtime, percentage, minutes_since_last_break, seconds)
            current_progress = round((time.time() - self.start_time) / self.end_time, 2)
            if current_progress != round(self.last_progress, 2):
                self.update_progress((time.time() - self.start_time) / self.end_time)
                self.last_progress = round(self.progress, 2)

        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()

    def crafting_part(self):
        self.log_msg("Selecting recipe")
        self.craft_bodies()
        time.sleep(self.random_sleep_length())
        self.recipeselector()
        time.sleep(self.random_sleep_length())
        if self.afk_train and self.is_runelite_focused():
            self.log_msg("Switching Window")
            pag.hotkey("alt", "tab")
        time.sleep(5)

    def craft_bodies(self):
        """
        Makes dragonhide bodies by click on each item and hitting space
        Returns:
            void
        Args:
            None
        """
        # get unique items in inventory
        unique_items = self.api_m.get_first_occurrence([self.leather_type, ids.NEEDLE])

        # move mouse to each item and click
        for item in unique_items:
            self.mouse.move_to(
                self.win.inventory_slots[item].random_point(),
                mouseSpeed="fastest",
                knotsCount=1,
                offsetBoundaryY=40,
                offsetBoundaryX=40,
                tween=pytweening.easeInOutQuad
                )
            self.mouse.click()
            time.sleep(self.random_sleep_length())

    def recipeselector(self):
        item_found = imsearch.search_img_in_rect(self.makemenu, self.win.chat, 0.05)
        search_time = time.time()
        while not item_found:
            item_found = imsearch.search_img_in_rect(self.makemenu, self.win.chat, 0.05)
            if time.time() - search_time > 12:
                self.log_msg("Can't find the menu, stopping the bot")
                self.log_msg("Furnace finder is " + self.menufinder)
                if self.menufinder:
                    self.log_msg("Stopping the bot")
                    self.logout()
                    self.stop()
                else:
                    self.log_msg("Retrying to find the menu")
                    self.menufinder = True
                    self.crafting_part()
                    return
            time.sleep(.1)
        time.sleep(self.random_sleep_length())
        self.log_msg("Starting to craft")
        pag.press("space")

    def alcher(self):
        slot_indices = self.api_m.get_inv_item_indices(self.toalch)
        alch_icon = imsearch.search_img_in_rect(self.highalchicon, self.win.control_panel, confidence=0.15)
        search_time = time.time()
        while not alch_icon:
            alch_icon = imsearch.search_img_in_rect(self.highalchicon, self.win.control_panel, confidence=0.15)
            if time.time() - search_time > 20:
                self.log_msg("Can't find the alchemy icon, stopping the bot")
                self.stop()
            time.sleep(.1)
        for index in slot_indices:
            if alch_icon:
                p = alch_icon.random_point()
                self.mouse.move_to(
                    p,
                    mouseSpeed="fastest",
                    knotsCount=1,
                    offsetBoundaryY=40,
                    offsetBoundaryX=40,
                    tween=pytweening.easeInOutQuad,
                )
                crossbow_icon = imsearch.search_img_in_rect(self.crossbowicon, self.win.control_panel, confidence=0.15)
                search_time = time.time()
                while not crossbow_icon:
                    crossbow_icon = imsearch.search_img_in_rect(self.crossbowicon, self.win.control_panel, confidence=0.15)
                    if time.time() - search_time > 20:
                        self.log_msg("Can't find the crossbow icon, stopping the bot")
                        self.stop()
                    time.sleep(.1)
                if index != 0:
                    time.sleep(self.random_sleep_length(0.5, 1.5))
                self.mouse.click()

            # clicks the dhide body in the inventory
            if index < 8 and len(slot_indices) >= 8:
                alchpoint = self.win.inventory_slots[7]
            else:
                alchpoint = self.win.inventory_slots[index]
            p = alchpoint.random_point()
            self.mouse.move_to(
                p,
                mouseSpeed="fastest",
                knotsCount=1,
                offsetBoundaryY=40,
                offsetBoundaryX=40,
                tween=pytweening.easeInOutQuad,
            )
            self.mouse.click()
            if len(self.api_m.get_inv_item_indices(self.toalch)) == 1:
                time.sleep(2)


    def unnotingonbank(self):
        notesslot = self.api_m.get_first_occurrence(self.unnoteid)
        if notesslot == -1:
            self.log_msg("You have no more dragon leather, quitting.")
            self.stop()
        else:
            self.mouse.move_to(
                self.win.inventory_slots[notesslot].random_point(),
                mouseSpeed="fastest",
                knotsCount=1,
                offsetBoundaryY=40,
                offsetBoundaryX=40,
                tween=pytweening.easeInOutQuad
                )
            self.mouse.click()

            if bank := self.get_all_tagged_in_rect(self.win.game_view, clr.YELLOW):
                bank = sorted(bank, key=RuneLiteObject.distance_from_rect_center)
                if len(bank) > 0:
                    self.log_msg("Found the bank.")
                    self.mouse.move_to(
                        bank[0].random_point(),
                        mouseSpeed="fastest",
                        knotsCount=1,
                        offsetBoundaryY=40,
                        offsetBoundaryX=40,
                        tween=pytweening.easeInOutQuad,
                    )
                    self.log_msg("Using on the bank")
                    self.mouse.click()
                    time.sleep(self.random_sleep_length())
            else:
                self.log_msg("Bank isn't found, quitting.")
                self.stop()

            unnotemenu_found = imsearch.search_img_in_rect(self.unnotemenu, self.win.chat, 0.05)
            search_time = time.time()
            while not unnotemenu_found:
                unnotemenu_found = imsearch.search_img_in_rect(self.unnotemenu, self.win.chat, 0.05)
                if time.time() - search_time > 12:
                    self.log_msg("Can't find the menu, stopping the bot")
                    self.log_msg("Unnote menu finder is " + self.unnotemenufinder)
                    if self.unnotemenufinder:
                        self.log_msg("Stopping the bot")
                        self.logout()
                        self.stop()
                    else:
                        self.log_msg("Retrying to find the menu")
                        self.unnotemenufinder = True
                        self.unnotingonbank()
                        return
                time.sleep(.1)
            time.sleep(self.random_sleep_length())
            self.log_msg("Pressing Yes")
            pag.press("1")
            time.sleep(0.6)

    def randombankclosing(self):
        choice = random.choice([1, 2])
        if choice == 1:
            self.close_bank()
        else:
            pag.press("esc")


    def withdrawrandomized(self):
        first_index = random.choice([0, 1])
        second_index = 1 if first_index == 0 else 0

        supplies_left = self.withdraw_items(self.withdraw_paths[first_index])
        if not supplies_left:
            self.log_msg("Out of supplies, stopping.")
            self.stop()

        supplies_left = self.withdraw_items(self.withdraw_paths[second_index])
        if not supplies_left:
            self.log_msg("Out of supplies, stopping.")
            self.stop()

    def idle_by_xp(self):
        timer = 0
        
        last_xp = self.get_total_xp()
        while timer < 5:                #pro-tip set this to a variable you can set via options 
            time.sleep(rd.fancy_normal_sample(.8,1.2)) 
            current_xp = self.get_total_xp()
            if current_xp > last_xp:
                last_xp = current_xp
                timer = 0
            else:
                timer += 1
        self.log_msg("Idle...")

    def setup(self):
        """Sets up loop variables, checks for required items, and checks location.
            Args:
                None
            Returns:
                None"""
        super().setup()
        self.withdraw_ids = [self.leather_type]
        self.withdraw_paths = [self.WILLOWSDAD_IMAGES.joinpath(self.bank_picture)]
        self.deposit_ids = []
        self.makemenu = self.WILLOWSDAD_IMAGES.joinpath("howmanymenu.png")
        self.highalchicon = self.WILLOWSDAD_IMAGES.joinpath("High_level_alchemy.png")
        self.crossbowicon = self.WILLOWSDAD_IMAGES.joinpath("Enchant_Crossbow_Bolt.png")
        self.unnotemenu = self.WILLOWSDAD_IMAGES.joinpath("unnotemenu.png")
    

    def sleep(self, percentage):
        """Sleeps for a random amount of time between the min and max delay. While player is doing an action.
            Args:
                None
            Returns:
                None"""
        self.breaks_skipped = 0
        afk_time = 0
        afk__start_time = time.time() 

        while self.api_m.get_first_occurrence(self.unstrung_bow) != -1:
            time.sleep(self.random_sleep_length(.65, 2.2))
            afk_time = int(time.time() - afk__start_time)
            self.breaks_skipped = afk_time // 15

        if self.breaks_skipped > 0:
            self.roll_chance_passed = True
            self.multiplier += self.breaks_skipped * .25
            self.log_msg(f"Skipped {self.breaks_skipped} break rolls while afk, percentage chance is now {round(percentage * 100)}%")

    
    def is_runelite_focused(self):
        """
        This will check if the runelite window is focused.
        Returns: boolean
        Args: None
        """
        # Get the currently focused window
        current_window = pag.getActiveWindow()

        # Check if the window title contains a certain keyword (e.g. "Google Chrome")
        if current_window is None:
            return False
        if "runelite" in current_window.title.lower():
            self.is_focused = True
            return True
        else:
            self.is_focused = False
            return False
    
    
    def random_sleep_length(self, delay_min=0, delay_max=0):
        """Returns a random float between min and max"""
        if delay_min == 0:
            delay_min = self.delay_min
        if delay_max == 0:
            delay_max = self.delay_max
        return rd.fancy_normal_sample(delay_min, delay_max)
    

    def open_tab(self, number):
        """
        This will open the specific tab chosen.

        Returns: void 

        args: number -> is the number of the specific tab you want to open. 
        -------------------------------------------------------------------
        number = 0  -> Combat-Tab 
        number = 1  -> Skills-Tab
        number = 2  -> Quest-Tab
        number = 3  -> Inventory-Tab
        number = 4  -> Equipment-Tab 
        number = 5  -> Prayer-Tab
        number = 6  -> Spellbook-Tab
        number = 7  -> Clan/Group-Tab
        number = 8  -> Friends-Tab
        number = 9  -> Account-Tab
        number = 10 -> Logout/Worldswitch-Tab
        number = 11 -> Settings-Tab
        number = 12 -> Emote-Tab
        number = 13 -> Music-Tab
        -------------------------------------------------------------------
        """
        if number < 0 or number > 13:
            self.log_msg("Choose a number between 0 and 13 as argument.")
            self.stop()
        else:
            self.mouse.move_to(self.win.cp_tabs[number].random_point())
            self.mouse.click()
            time.sleep(self.random_sleep_length())
