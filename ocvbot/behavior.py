import logging as log
import random as rand
import time

import pyautogui as pag

from ocvbot import input, misc, vision
from ocvbot import DISPLAY_HEIGHT, DISPLAY_WIDTH

# TODO

"""
def chat(context)
  if context == 'smelting'
    type 'option 1'
    type 'option 2'
  
  elif context == 'blablabla'
  
def move_camera_rand(chance=3,down_min=200,down_max=2000)
    down_arrow_roll = rand.randint(1, chance)
    if down_arrow_roll == chance:
       input.keyDown('Down')
       time.sleep(float(rand.randint(down_min, down_max)))
       input.keyUp('Down')
    left
    right arrow roll
 
def check_experience(skill)

def switch_worlds()
"""


def login(username_file='username.txt', password_file='password.txt',
          cred_sleep_min=800, cred_sleep_max=5000,
          login_sleep_min=500, login_sleep_max=5000,
          postlogin_sleep_min=500, postlogin_sleep_max=5000):
    """
    Logs in in using credentials specified in two files.

    Args:
        username_file (file): The filepath of the file containing the
                              user's username. Filepath is relative to
                              the directory this file is in, default is
                              a file simply called "username".
        password_file (file): The filepath of the file containing the
                              user's password. Filepath is relative to
                              the directory this file is in, default is
                              a file simply called "password".
        cred_sleep_min (int): The minimum number of miliseconds to wait
                              between actions while entering account
                              credentials, default is 800.
        cred_sleep_max (int): The maximum number of miliseconds to wait
                              between actions while entering account
                              credentials, default is 5000.
        login_sleep_min (int): The minimum number of miliseconds to wait
                               after hitting "Enter" to login, default
                               is 5000.
        login_sleep_max (int): The maximum number of miliseconds to wait
                               after hitting "Enter" to login, default
                               is 15000.
        postlogin_sleep_min (int): The minimum number of miliseconds to
                                   wait after clicking the "Click here
                                   to play" button, default is 5000.
        postlogin_sleep_max (int): The maximum number of miliseconds to
                                   wait after clicking the "Click here
                                   to play" button, default is 10000.

    Raises:
        Raises a runtime error if the login menu cannot be found, the
        postlogin screen cannot be found, or the logged-in client cannot
        be found.

    Returns:
        Always returns 0.
    """

    from ocvbot.vision import vdisplay

    # Check to make extra sure the client is logged out.
    logged_out = vdisplay.click_image(needle='./needles/login-menu/'
                                             'orient-logged-out.png',
                                      loop_num=1)
    if logged_out == 1:
        raise RuntimeError("Cannot find client!")

    log.info('Logging in.')

    # Click the "Ok" button if it's present at the login screen.
    vdisplay.click_image(needle='./needles/login-menu/'
                                'ok-button.png',
                                loop_num=1)

    misc.sleep_rand(cred_sleep_min, cred_sleep_max)

    # Make sure the "Existing user" button is present.
    existing_user = vdisplay.wait_for_image(needle='./needles/login-menu/'
                                            'existing-user-button.png',
                                            loop_num=1)
    if existing_user != 1:

        # Enter credentials.
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        input.keypress('enter')
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        pag.typewrite(open(username_file, 'r').read())
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        pag.typewrite(open(password_file, 'r').read())
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        input.keypress('enter')
        misc.sleep_rand(login_sleep_min, login_sleep_max)

        # Click the 'click here to play' button in the postlogin menu.
        postlogin = vdisplay.click_image(needle='./needles/'
                                         'login-menu/orient-postlogin.png',
                                         conf=0.8,
                                         loop_num=50,
                                         loop_sleep_min=1000,
                                         loop_sleep_max=3000)
        if postlogin != 1:
            misc.sleep_rand(postlogin_sleep_min, postlogin_sleep_max)
            # Wait for the orient.png to appear in the client window.
            logged_in = vdisplay.wait_for_image(needle='./needles/minimap/'
                                                'orient.png',
                                                loop_num=50,
                                                loop_sleep_min=1000,
                                                loop_sleep_max=3000)
            if logged_in != 1:
                # Make sure client camera is oriented correctly after
                #   logging in.
                pag.keyDown('Up')
                misc.sleep_rand(3000, 7000)
                pag.keyUp('Up')
                return 0
            else:
                raise RuntimeError("Cannot login!")

        else:
            raise RuntimeError("Cannot find postlogin screen!")

    elif existing_user == 1:
        raise RuntimeError("Cannot find existing user button!")


def wait_rand(chance, second_chance=10,
              wait_min=10000, wait_max=60000):
    """
    Roll for a chance to do nothing for the specified period of time.

    Args:
        chance (int): The number that must be rolled for the wait to be
                      called. For example, if change is 25, then there
                      is a 1 in 25 chance for the roll to pass.
        second_chance (int): The number that must be rolled for an
                             additional wait to be called if the first
                             roll passes, default is 10. By default,
                             this means that 10% of waits that pass the
                             first roll wait for an additional period of
                             time.
        wait_min (int): The minimum number of miliseconds to wait if the
                        roll passes, default is 10000.
        wait_max (int): The maximum number of miliseconds to wait if the
                        roll passes, default is 60000.

    Returns:
        Always returns 0.
    """

    wait_roll = rand.randint(1, chance)
    if wait_roll == chance:
        log.info('Random wait called.')
        sleeptime = misc.rand_seconds(wait_min, wait_max)
        log.info('Sleeping for ' + str(round(sleeptime)) + ' seconds.')
        time.sleep(sleeptime)

        # Perform an additional wait roll so that (1/second_chance)
        #   waits are extra long.
        wait_roll = rand.randint(1, second_chance)
        if wait_roll == 10:
            log.info('Additional random wait called.')
            sleeptime = misc.rand_seconds(wait_min, wait_max)
            log.info('Sleeping for ' + str(round(sleeptime)) + ' seconds.')
            time.sleep(sleeptime)
    return 0


def open_side_stone(side_stone_open, hotkey):
    from ocvbot.vision import vclient, vgame_screen
    stone_open = vclient.wait_for_image(needle=side_stone_open, loop_num=1)
    if stone_open != 1:
        log.debug('Side stone already open')
        return 0

    # If side stone is not already open, check to make sure the bank
    #   window is not blocking it.
    vgame_screen.click_image(needle='./needles/buttons/bank-close.png',
                             loop_num=2,
                             loop_sleep_min=500, loop_sleep_max=1000)

    # Try a total of 5 times to open the desired side stone menu using
    #   the hotkey.
    for tries in range(1, 5):
        input.keypress(hotkey)
        stone_open = vclient.wait_for_image(needle=side_stone_open,
                                            loop_num=10,
                                            loop_sleep_min=1000,
                                            loop_sleep_max=3000)
        if stone_open != 1:
            log.info('Opened side stone')
            return 0
    log.error('Could not open side stone! Is the hotkey correct?')
    return 1


def logout(hotkey):
    """
    If the client is logged in, logs out. Side stone hotkeys MUST be
    enabled.

    Raises:
        Raises a runtime error if the logout side stone is opened but
        the logout button cannot be found.

    Returns:
        Returns 0 if the client has logged out.
        Returns 1 if the client is already logged out.
    """
    # TODO: Check if the world-switcher is open in the login menu.

    from ocvbot.vision import vclient
    # First, make sure the client is logged in.
    orient = vision.orient(display_height=DISPLAY_HEIGHT,
                           display_width=DISPLAY_WIDTH)
    (client_status, unused_var) = orient
    if client_status == 'logged_in':
        open_side_stone('./needles/side-stones/logout', hotkey=hotkey)
        logout_button = vclient.click_image(needle='./needles/buttons/'
                                                   'logout.png')
        if logout_button != 1:
            logged_out = vclient.wait_for_image(needle='./needles/login-menu/'
                                                'orient-logged-out.png',
                                                loop_num=50,
                                                loop_sleep_min=1000,
                                                loop_sleep_max=3000)
            if logged_out != 1:
                log.info('Logged out')
                return 0
            for tries in range(1, 10):
                vclient.click_image(needle='./needles/buttons/'
                                           'logout.png')
                logged_out = vclient.wait_for_image(needle='./needles/'
                                                    'login-menu/'
                                                    'orient-logged-out.png',
                                                    loop_num=30,
                                                    loop_sleep_min=1000,
                                                    loop_sleep_max=1500)
                if logged_out != 1:
                    log.info('Logged out after trying' + str(tries) +
                             'time(s)')
                    return 0
                raise RuntimeError("Could not logout!")
        elif logout_button == 1:
            raise RuntimeError("Could not find logout button!")

    elif client_status == 'logged_out':
        log.warning("Client already logged out!")
        return 1
    else:
        return 0


def logout_rand(chance, wait_min=5, wait_max=120):
    """
    Random chance to logout of the client and wait. Units are in minutes.

    Args:
        chance (int): See wait_rand()'s docstring.
        wait_min (int): The minimum number of minutes to wait if the
                        roll passes, default is 5.
        wait_max (int): The maximum number of minutes to wait if the
                        roll passes, default is 120.

    Returns:
        Always returns 0.
    """

    # Convert to miliseconds.
    wait_min *= 60000
    wait_max *= 60000

    logout_roll = rand.randint(1, chance)
    if logout_roll == chance:
        log.info('Random logout called.')
        #logout()

        sleeptime = misc.rand_seconds(wait_min, wait_max)
        # Convert to minutes for logging
        sleeptime_minutes = sleeptime / 60000
        log.info('Sleeping for ' + str(sleeptime_minutes) + 'minutes.')
        time.sleep(sleeptime)
    return 0


def drop_item(item, track=True,
              wait_chance=120, wait_min=5000, wait_max=20000):
    """
    Drops all instances of the provided item from the inventory.
    Shift+Click to drop item MUST be enabled.

    Args:
       item (file): Filepath to an image of the item to drop, as it
                    appears in the player's inventory.
       track (bool): Keep track of the number of items dropped in a
                     global variable, default is True.
       wait_chance (int): Chance to wait randomly while dropping item,
                          see wait_rand()'s docstring for more info,
                          default is 50.
       wait_min (int): Minimum number of miliseconds to wait if
                       a wait is triggered, default is 5000.
       wait_max (int): Maximum number of miliseconds to wait if
                       a wait is triggered, default is 20000.
    """
    # TODO: create four objects, one for each quadrant of the inventory
    #   and rotate dropping items randomly among each quadrant to make
    #   item-dropping more randomized.

    from ocvbot.vision import vinv, vinv_right_half, vinv_left_half, vclient
    from ocvbot import items

    # Make sure the inventory tab is selected in the main menu.
    log.info('Making sure inventory is selected')
    inv_selected = vclient.wait_for_image(needle='./needles/side-stones/'
                                                 'inventory-selected.png')
    if inv_selected == 1:
        input.keypress('Escape')

    item_remains = vinv.wait_for_image(loop_num=1, needle=item)

    if item_remains != 1:
        log.info('Dropping ' + str(item) + '.')
    elif item_remains == 1:
        log.info('Could not find ' + str(item) + '.')
        return 1

    tries = 0
    while item_remains != 1 and tries <= 40:

        tries += 1
        pag.keyDown('shift')
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        item_on_right = vinv_right_half.click_image(loop_num=1,
                                                    click_sleep_befmin=10,
                                                    click_sleep_befmax=50,
                                                    click_sleep_afmin=50,
                                                    click_sleep_afmax=300,
                                                    move_durmin=50,
                                                    move_durmax=800,
                                                    needle=item)
        if item_on_right != 1 and track is True:
            items += 1
        item_on_left = vinv_left_half.click_image(loop_num=1,
                                                  click_sleep_befmin=10,
                                                  click_sleep_befmax=50,
                                                  click_sleep_afmin=50,
                                                  click_sleep_afmax=300,
                                                  move_durmin=50,
                                                  move_durmax=800,
                                                  needle=item)
        if item_on_left != 1 and track is True:
            items += 1

        # Search the entire inventory to check if the item is still
        #   there.
        item_remains = vinv.wait_for_image(loop_num=1, needle=item)

        # Chance to briefly wait while dropping items.
        wait_rand(chance=wait_chance, wait_min=wait_min, wait_max=wait_max)

        pag.keyUp('shift')
        if item_remains == 1:
            return 0

    if tries > 40:
        log.error('Tried dropping item too many times!')
        return 1
    else:
        return 0
