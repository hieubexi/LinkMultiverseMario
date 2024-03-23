from engine import *



click_delay = 10
click_timer = 0
clickable = True


def move_right_key_pressed():
    return (is_key_down("d") or
            is_key_down('right'))


def move_left_key_pressed():
    return (is_key_down("a") or
            is_key_down('left'))


def jump_key_pressed():
    return (is_key_down("w") or
            is_key_down('up') or
            is_key_down('space') )


def attack_key_pressed():
    return (is_key_down("shift") )


def skip_key_pressed():
    return (is_key_down("space"))


def return_key_pressed():
    return (is_key_down("return") )


def pause_key_pressed():
    return (is_key_down("esc"))

