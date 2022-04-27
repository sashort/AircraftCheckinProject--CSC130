import time
import os

import Flight

os.system("")
styles = dict()
colors = dict()

__default_menu_width__ = 30


class Style:
    def __init__(self, *, bold=False, italic=False, underlined=False, strikethrough=False, outlined=False,
                 inverted=False, background_color=None, foreground_color=None, background_gradient_color_left=None,
                 background_gradient_color_right=None, foreground_gradient_color_left=None,
                 foreground_gradient_color_right=None):
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.outlined = outlined
        self.inverted = inverted
        if background_color is not None:
            if isinstance(background_color, str):
                self.background_color = colors[background_color]
            else:
                self.background_color = background_color
        else:
            self.background_color = None
        if foreground_color is not None:
            if isinstance(foreground_color, str):
                self.foreground_color = colors[foreground_color]
            else:
                self.foreground_color = foreground_color
        else:
            self.foreground_color = None
        if background_gradient_color_left is not None:
            if isinstance(background_gradient_color_left, str):
                self.background_gradient_color_left = colors[background_gradient_color_left]
            else:
                self.background_gradient_color_left = background_gradient_color_left
        else:
            self.background_gradient_color_left = None
        if background_gradient_color_right is not None:
            if isinstance(background_gradient_color_right, str):
                self.background_gradient_color_right = colors[background_gradient_color_right]
            else:
                self.background_gradient_color_right = background_gradient_color_right
        else:
            self.background_gradient_color_right = None
        if foreground_gradient_color_left is not None:
            if isinstance(foreground_gradient_color_left, str):
                self.foreground_gradient_color_left = colors[foreground_gradient_color_left]
            else:
                self.foreground_gradient_color_left = foreground_gradient_color_left
        else:
            self.foreground_gradient_color_left = None
        if foreground_gradient_color_right is not None:
            if isinstance(foreground_gradient_color_right, str):
                self.foreground_gradient_color_right = colors[foreground_gradient_color_right]
            else:
                self.foreground_gradient_color_right = foreground_gradient_color_right
        else:
            self.foreground_gradient_color_right = None

    __applied_styles__ = list()
    __defined_colors__ = dict()
    __bold__ = 0
    __italic__ = 0
    __underlined__ = 0
    __strikethrough__ = 0
    __inverted__ = 0
    __outlined__ = 0
    __bypass_call__ = False


def __current_formatting__():
    my_str = "\033[0m"
    if Style.__bold__ > 0:
        my_str += "\033[1m"
    if Style.__italic__ > 0:
        my_str += "\033[3m"
    if Style.__underlined__ > 0:
        my_str += "\033[4m"
    if Style.__strikethrough__ > 0:
        my_str += "\033[9m"
    if Style.__outlined__ > 0:
        my_str += "\033[51m"
    if Style.__inverted__ % 2 != 0:
        my_str += "\033[7m"
    bg = None
    fg = None
    for curr_style in reversed(Style.__applied_styles__):
        if bg is None and curr_style.background_color is not None:
            bg = curr_style.background_color
        if fg is None and curr_style.foreground_color is not None:
            fg = curr_style.foreground_color
        if fg is not None and bg is not None:
            break
    if bg is not None:
        my_color = None
        if isinstance(bg, str):
            my_color = Style.__defined_colors__[bg]
        elif isinstance(bg, tuple):
            my_color = bg
        my_str += "\33[48;2;" + str(my_color[0]) + ";" + str(my_color[1]) + ";" + str(my_color[2]) + "m"
    if fg is not None:
        my_color = None
        if isinstance(fg, str):
            my_color = Style.__defined_colors__[fg]
        elif isinstance(fg, tuple):
            my_color = fg
        my_str += "\33[38;2;" + str(my_color[0]) + ";" + str(my_color[1]) + ";" + str(my_color[2]) + "m"
    return my_str


def apply_style(style):
    my_style = None
    if isinstance(style, str):
        my_style = styles[style]
    else:
        my_style = style
    Style.__applied_styles__.append(my_style)
    if my_style.bold:
        Style.__bold__ += 1
    if my_style.italic:
        Style.__italic__ += 1
    if my_style.underlined:
        Style.__underlined__ += 1
    if my_style.strikethrough:
        Style.__strikethrough__ += 1
    if my_style.outlined:
        Style.__outlined__ += 1
    if my_style.inverted:
        Style.__inverted__ += 1
    if not Style.__bypass_call__:
        print(__current_formatting__())


def pop_style():
    if len(Style.__applied_styles__) > 0:
        my_style = Style.__applied_styles__.pop()
        if my_style.bold:
            Style.__bold__ -= 1
        if my_style.italic:
            Style.__italic__ -= 1
        if my_style.underlined:
            Style.__underlined__ -= 1
        if my_style.strikethrough:
            Style.__strikethrough__ -= 1
        if my_style.outlined:
            Style.__outlined__ -= 1
        if my_style.inverted:
            Style.__inverted__ -= 1
        if not Style.__bypass_call__:
            print(__current_formatting__())


def styled(style, my_text):
    my_str = ""
    my_style = None
    if isinstance(style, str):
        my_style = styles[style]
    else:
        my_style = style
    Style.__bypass_call__ = True
    apply_style(my_style)
    my_str = __current_formatting__()
    pop_style()
    Style.__bypass_call__ = False
    text_list = [char for char in my_text]
    if isinstance(my_style, str):
        input("Somehow my_style is still a string")
    if my_style.background_gradient_color_left is not None and my_style.background_gradient_color_right is not None:
        step = (
            (my_style.background_gradient_color_right[0] - my_style.background_gradient_color_left[0]) / len(text_list),
            (my_style.background_gradient_color_right[1] - my_style.background_gradient_color_left[1]) / len(text_list),
            (my_style.background_gradient_color_right[2] - my_style.background_gradient_color_left[2]) / len(text_list))
        curr_bg_color = [my_style.background_gradient_color_left[0], my_style.background_gradient_color_left[1],
                         my_style.background_gradient_color_left[2]]
        for bg in range(len(text_list)):
            text_list[bg] = "\33[48;2;" + str(int(curr_bg_color[0])) + ";" + str(int(curr_bg_color[1])) + ";" + str(
                int(curr_bg_color[2])) + "m" + text_list[bg]
            curr_bg_color[0] += step[0]
            curr_bg_color[1] += step[1]
            curr_bg_color[2] += step[2]
    if my_style.foreground_gradient_color_left is not None and my_style.foreground_gradient_color_right is not None:
        step = (
            (my_style.foreground_gradient_color_right[0] - my_style.foreground_gradient_color_left[0]) / len(text_list),
            (my_style.foreground_gradient_color_right[1] - my_style.foreground_gradient_color_left[1]) / len(text_list),
            (my_style.foreground_gradient_color_right[2] - my_style.foreground_gradient_color_left[2]) / len(text_list))
        curr_fg_color = [my_style.foreground_gradient_color_left[0], my_style.foreground_gradient_color_left[1],
                         my_style.foreground_gradient_color_left[2]]
        for fg in range(len(text_list)):
            text_list[fg] = "\33[38;2;" + str(int(curr_fg_color[0])) + ";" + str(int(curr_fg_color[1])) + ";" + str(
                int(curr_fg_color[2])) + "m" + text_list[fg]
            curr_fg_color[0] += step[0]
            curr_fg_color[1] += step[1]
            curr_fg_color[2] += step[2]
    new_text = ""
    for section in text_list:
        new_text += section
    return my_str + new_text + __current_formatting__()


class MenuItem:
    def __init__(self, menu, key):
        self.__menu__ = menu
        self.__key__ = key

    def disabled(self):
        return self.__key__ in self.__menu__.__disabled_items__

    def hidden(self):
        return self.__key__ in self.__menu__.__hidden_items__

    def set_disabled(self, value):
        if value and self.__key__ not in self.__menu__.__disabled_items__:
            self.__menu__.__disabled_items__.append(self.__key__)
        elif not value and self.__key__ in self.__menu__.__disabled_items__:
            self.__menu__.__disabled_items__.remove(self.__key__)

    def set_hidden(self, value):
        if value and self.__key__ not in self.__menu__.__hidden_items__:
            self.__menu__.__hidden_items__.append(self.__key__)
        elif not value and self.__key__ in self.__menu__.__hidden_items__:
            self.__menu__.__hidden_items__.remove(self.__key__)


class Menu:
    def __init__(self, title, menu_items, *, exit_value=None, invalid_return_value=-1, not_available_return_value=-2):
        self.title = title
        self.menu_items = menu_items
        self.exit_value = exit_value
        self.invalid_return_value = invalid_return_value
        self.__message_style__ = None
        self.__message__ = None
        self.__hidden_items__ = list()
        self.__disabled_items__ = list()
        self.not_available_return_value = not_available_return_value

    def menu_item(self, key):
        if key in self.menu_items.keys():
            return MenuItem(self, key)

    def set_message(self, message, style):
        self.__message__ = message
        if style is not None:
            if isinstance(style, str):
                self.__message_style__ = styles[style]
            else:
                self.__message_style__ = style

    def menu_item(self, key):
        return MenuItem(self, key)

    def show(self, prompt=None, *, center_message=True, indent=0, show_available_seats=False, default_value=None,
             sticky_message=False, show_title_first=False):
        response = None
        indent_str = ""
        if indent > 0:
            for i in range(indent):
                indent_str += '\t'
        while response is None:
            for i in range(100):
                print()
            if show_available_seats:
                Flight.show_available_seats()
                print()
            title_lines = self.title.replace('\r', '').split('\n')
            menu_width = 0
            for ln in title_lines:
                menu_width = max(menu_width, len(ln))
            message_lines = list()
            keys = list(self.menu_items.keys())
            max_key_length = 0
            style = None
            if self.__message__ is not None:
                if self.__message_style__ is not None:
                    style = self.__message_style__
                else:
                    style = self.__message_style__
                for line in self.__message__.replace('\r', "").split('\n'):
                    message_lines.append(line)
                    if len(line) > menu_width:
                        menu_width = len(line)
            max_key_length = 0
            max_menu_item_length = 0
            default_found = False
            for key in keys:
                if key not in self.__hidden_items__:
                    key_str = str(key)
                    if key_str == str(default_value):
                        key_str = '<' + key_str + '>'
                        default_found = True
                    max_key_length = max(max_key_length, len(key_str))
                    max_menu_item_length = max(max_menu_item_length, len(self.menu_items[key]))
            menu_width = max(max(menu_width, max_key_length + max_menu_item_length + 1) + 2, __default_menu_width__)
            if self.title is not None and self.title != "" and show_title_first:
                if self.__message__ is None:
                    print(indent_str + styled("Menu Title", ''.center(menu_width)))
                for ttl_ln in title_lines:
                    print(indent_str + styled("Menu Title", ttl_ln.center(menu_width)))
                if self.__message__ is None:
                    print(indent_str + styled("Menu Title", ''.center(menu_width)))
            if self.__message__ is not None:
                print(indent_str + styled("Menu Title" if style is None else style, ''.ljust(menu_width)))
                for line in message_lines:
                    result = line.center(menu_width) if center_message else (' ' + line).ljust(menu_width)
                    print(indent_str + styled("Menu Title" if style is None else style, result))
                print(indent_str + styled("Menu Title" if style is None else style, ''.ljust(menu_width)))
            if self.title is not None and self.title != "" and not show_title_first:
                if self.__message__ is None:
                    print(indent_str + styled("Menu Title", ''.center(menu_width)))
                for ttl_ln in title_lines:
                    print(indent_str + styled("Menu Title", ttl_ln.center(menu_width)))
                if self.__message__ is None:
                    print(indent_str + styled("Menu Title", ''.center(menu_width)))
            for key in keys:
                if key not in self.__hidden_items__:
                    key_str = str(key).rjust(max_key_length - 2)
                    if str(key) == str(default_value):
                        key_str = "<" + key_str.rjust(max_key_length - 2) + ">"
                    elif default_found:
                        key_str = (key_str + ' ').rjust(max_key_length)
                    else:
                        key_str = key_str.rjust(max_key_length)
                    if key in self.__disabled_items__:
                        print(indent_str + styled("Disabled Menu Item", (key_str + " " + self.menu_items[key].ljust(max_menu_item_length)).center(menu_width)))
                    else:
                        print(indent_str + styled("Menu Item", (key_str + " " + self.menu_items[key].ljust(max_menu_item_length)).center(menu_width)))
            if not sticky_message:
                self.__message_style__ = None
                self.__message__ = None

            if prompt is not None:
                matched = False
                prompt_lines = prompt.replace('\r', '').split('\n')
                prompt = indent_str + prompt_lines[0]
                for i in range(len(prompt_lines) - 1):
                    prompt += '\n' + indent_str + prompt_lines[i + 1]
                response = input(prompt)
                if response == '':
                    if default_value is not None:
                        response = default_value
                    else:
                        response = None
                elif len(self.menu_items) == 0:
                    try:
                        return int(response)
                    except ValueError:
                        return response
                elif response in self.menu_items.keys():
                    pass
                elif response.upper() in self.menu_items.keys():
                    matched = True
                    response = response.upper()
                elif len(self.menu_items) == 1 and self.exit_value in self.menu_items.keys():
                    try:
                        response = int(response)
                    except ValueError:
                        pass
                elif response not in self.menu_items.keys():
                    response = response.upper()
                    for key in self.menu_items.keys():
                        if response == str(key).upper():
                            matched = True
                            response = key
                            break
                    if not matched:
                        response = self.invalid_return_value
                else:
                    break
                if matched and (response in self.__disabled_items__ or response in self.__hidden_items__):
                    response = self.not_available_return_value
        if sticky_message:
            self.__message_style__ = None
            self.__message__ = None
        return response


# Color definitions
colors["Red"] = (255, 0, 0)
colors["Green"] = (53, 94, 59)
colors["Orange"] = (255, 112, 0)
colors["Blue"] = (0, 0, 120)
colors["Neon Red"] = (255, 7, 58)
colors["Candy Apple Red"] = (100, 3, 0)
colors["Burnt Orange"] = (80, 33, 0)
colors["Neon Orange"] = (255, 95, 31)
colors["White"] = (255, 255, 255)
colors["Dark Grey"] = (68, 68, 68)
colors["Darker Grey"] = (40, 40, 40)
colors["Black"] = (0, 0, 0)
colors["Almost White"] = (180, 180, 180)

# Generic Styles
styles["Underlined"] = Style(underlined=True)
styles["Outlined"] = Style(outlined=True)
styles["Inverted"] = Style(inverted=True)
styles["Bold"] = Style(bold=True)

# Menu Message Header Styles
styles["Information"] = Style(background_gradient_color_left=(11, 11, 69), background_gradient_color_right="Black", bold=True)
styles["Confirmation"] = Style(background_color="Green")
styles["Caution"] = Style(background_gradient_color_left="Neon Orange", background_gradient_color_right="Burnt Orange", foreground_color="Black", bold=True)
styles["Error"] = Style(background_gradient_color_left="Neon Red", background_gradient_color_right="Candy Apple Red", bold=True)

# UI Specific Styles
styles["Passenger List Banner"] = styles["Information"]
styles["Column Header"] = Style(bold=True, underlined=True)
styles["Error Message"] = Style(foreground_color="Red")
styles["Caution Message"] = Style(foreground_color="Orange")
styles["Menu Item"] = Style(background_gradient_color_left=(40, 40, 40),
                            background_gradient_color_right=(175, 175, 175), foreground_color="White")
styles["Disabled Menu Item"] = Style(background_gradient_color_left=(40, 40, 40),
                                     background_gradient_color_right=(175, 175, 175),
                                     foreground_gradient_color_left="Dark Grey",
                                     foreground_gradient_color_right="Darker Grey")
styles["Menu Title"] = Style(background_gradient_color_left="Almost White",
                             background_gradient_color_right="White", foreground_color="Black",
                             bold=True)


def passenger_string(passenger=None, *, index=0, underlined=False):
    if passenger is not None:
        index_str = ("" if index == 0 else str(index)).rjust(Flight.__field_widths__["Number"])
        if underlined:
            return styled("Underlined", " ".join(
                (index_str,
                 passenger.confirmation_id,
                 passenger.boarding_id.rjust(3),
                 passenger.boarding_group().rjust(Flight.__field_widths__["Boarding Group"]),
                 passenger.last_name.rjust(Flight.__field_widths__["Last Name"]),
                 passenger.first_name.rjust(Flight.__field_widths__["First Name"]))))
        else:
            return " ".join((index_str,
                             passenger.confirmation_id,
                             passenger.boarding_id.rjust(3),
                             passenger.boarding_group().rjust(Flight.__field_widths__["Boarding Group"]),
                             passenger.last_name.rjust(Flight.__field_widths__["Last Name"]),
                             passenger.first_name.rjust(Flight.__field_widths__["First Name"])))
    else:
        return " ".join(("".rjust(Flight.__field_widths__["Number"]),
                         styled("Underlined", "CONF #"),
                         styled("Underlined", "BID"),
                         styled("Underlined", "Boarding Group".rjust(Flight.__field_widths__["Boarding Group"])),
                         styled("Underlined", "Last".rjust(Flight.__field_widths__["Last Name"])),
                         styled("Underlined", "First".rjust(Flight.__field_widths__["First Name"]))))


def display_passenger_list(look_at, title="PASSENGER LIST", sort=True, delay_between_entries=0, index_list=None):
    def related(lst, index1, index2):
        if index1 < 0 or index2 >= len(lst):
            return False
        if isinstance(lst[index1], Flight.DisabledPassenger) and isinstance(lst[index2], Flight.AttendantPassenger) and \
                lst[index1].attendant is lst[index2]:
            return True
        elif isinstance(lst[index1], Flight.AttendantPassenger) and isinstance(lst[index2],
                                                                               Flight.DisabledPassenger) and \
                lst[index2].attendant is lst[index1]:
            return True
        elif isinstance(lst[index1], Flight.ParentPassenger) and isinstance(lst[index2], Flight.ParentPassenger) and \
                lst[index1].spouse is lst[index2]:
            return True
        elif isinstance(lst[index1], Flight.ParentPassenger) and isinstance(lst[index2], Flight.ChildPassenger) and \
                lst[index2] in lst[index1].children:
            return True
        elif isinstance(lst[index2], Flight.ParentPassenger) and isinstance(lst[index1], Flight.ChildPassenger) and \
                lst[index1] in lst[index2].children:
            return True
        elif isinstance(lst[index1], Flight.ChildPassenger) and isinstance(lst[index2], Flight.ChildPassenger) and \
                lst[index1].__parent__ is lst[index2].__parent__:
            return True
        return False

    for i in range(100):
        print()
    print("".rjust(Flight.total_field_width(), "─"))
    print(styled("Passenger List Banner", "".center(Flight.total_field_width())))
    print(styled("Passenger List Banner", title.center(Flight.total_field_width())))
    print(styled("Passenger List Banner", "".center(Flight.total_field_width())))
    print()
    Flight.show_available_seats()
    print()
    time.sleep(1)
    print(passenger_string())
    count = 1
    if sort:
        look_at.sort()
    prev_passenger = None
    for i in range(len(look_at)):
        passenger = look_at[i]
        if index_list is not None:
            index = index_list.index(passenger) + 1
        else:
            index = i + 1
        print(passenger_string(passenger, underlined=
        i < len(look_at) - 1 and passenger.boarding_group() != look_at[i + 1].boarding_group() or i == len(
            look_at) - 1, index=index), end='')

        if related(look_at, i - 1, i):
            if related(look_at, i, i + 1):
                print(" │", end="")
            else:
                print(" ╯", end="")
        elif related(look_at, i, i + 1):
            print(" ╮", end="")
        else:
            print("  ", end="")
        if isinstance(passenger, Flight.ChildPassenger):
            print(" 👶")
        elif isinstance(passenger, Flight.DisabledPassenger):
            print(" ♿")
        else:
            print()
        count += 1
        prev_passenger = passenger
        if delay_between_entries > 0:
            time.sleep(delay_between_entries)
    input(styled("Inverted", "DOUBLE TAP TO ENTER TO CONTINUE".center(Flight.total_field_width())))
