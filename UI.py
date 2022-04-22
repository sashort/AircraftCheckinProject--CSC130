import sys

styles = dict()
colors = dict()


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
    def __init__(self, title, menu_items, exit_value, *, invalid_return_value=-1, not_available_return_value=-2):
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

    def show(self, prompt=None, *, center_message=True, indent=0):
        response = None
        while response is None:
            for i in range(100):
                print()
            indent_str = ""
            if indent > 0:
                for i in range(indent):
                    indent_str += '\t'
            menu_width = len(self.title)
            message_lines = list()
            keys = list(self.menu_items.keys())
            max_key_length = 0
            max_menu_item_length = 0
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
            for key in keys:
                if key not in self.__hidden_items__:
                    if len(str(key)) > max_key_length:
                        max_key_length = len(str(key))
                    if len(self.menu_items[key]) > max_menu_item_length:
                        max_menu_item_length = len(self.menu_items[key])
            if max_key_length + max_menu_item_length + 1 > menu_width:
                menu_width = max_key_length + max_menu_item_length + 1
            print(indent_str + "╭" + "".rjust(menu_width + 2, "─") + "╮")
            print(indent_str + "│" + self.title.center(menu_width + 2) + "│")
            if self.__message__ is not None:
                for line in message_lines:
                    result = line.center(menu_width) if center_message else line.ljust(menu_width)
                    result = ' ' + result + ' '
                    if style is not None:
                        print(indent_str + "│" + styled(style, result) + "│")
                    else:
                        print(indent_str + "│" + result + "│")
            print(indent_str + "├" + "".ljust(menu_width + 2, "─") + "┤")
            for key in keys:
                if key not in self.__hidden_items__:
                    if key in self.__disabled_items__:
                        print(indent_str + "│ " + styled("Disabled", (
                                    str(key).rjust(max_key_length) + " " + self.menu_items[key]).ljust(
                            menu_width)) + " │")
                    else:
                        print(indent_str + "│ " + (str(key).rjust(max_key_length) + " " + self.menu_items[key]).ljust(
                            menu_width) + " │")
            print(indent_str + "╰" + "".rjust(menu_width + 2, "─") + "╯")
            self.__message_style__ = None
            self.__message__ = None

            if prompt is not None:
                response = input(indent_str + prompt)
                if response == '':
                    response = None
                elif response not in self.menu_items.keys():
                    matched = False
                    response = response.upper()
                    for key in self.menu_items.keys():
                        if response == str(key).upper():
                            matched = True
                            if key not in self.__hidden_items__ and key not in self.__disabled_items__:
                                response = key
                            else:
                                response = self.not_available_return_value
                            break
                    if not matched:
                        response = self.invalid_return_value
            else:
                break
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
colors["Black"] = (0, 0, 0)

# Generic Styles
styles["Underlined"] = Style(underlined=True)
styles["Outlined"] = Style(outlined=True)
styles["Inverted"] = Style(inverted=True)

# Menu Message Header Styles
styles["Information"] = Style(background_gradient_color_left=(11, 11, 69), background_gradient_color_right=(0, 0, 0))
styles["Confirmation"] = Style(background_color="Green")
styles["Caution"] = Style(background_gradient_color_left="Neon Orange", background_gradient_color_right="Burnt Orange")
styles["Error"] = Style(background_gradient_color_left="Neon Red", background_gradient_color_right="Candy Apple Red")

# UI Specific Styles
styles["Passenger List Banner"] = Style(background_gradient_color_left="Orange",
                                        background_gradient_color_right="Burnt Orange", foreground_color="Black",
                                        bold=True)
styles["Column Header"] = Style(bold=True, underlined=True)
styles["Error Message"] = Style(foreground_color="Red")
styles["Caution Message"] = Style(foreground_color="Orange")
styles["Disabled"] = Style(foreground_color="Dark Grey")
