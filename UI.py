import sys
themes = dict()


class Theme:
    def __init__(self, *, bold=False, italic=False, underlined=False, strikethrough=False, outlined=False,
                 inverted=False, background_color=None, foreground_color=None):
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.outlined = outlined
        self.inverted = inverted
        self.background_color = background_color
        self.foreground_color = foreground_color

    __applied_themes__ = list()
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
    if Theme.__bold__ > 0:
        my_str += "\033[1m"
    if Theme.__italic__ > 0:
        my_str += "\033[3m"
    if Theme.__underlined__ > 0:
        my_str += "\033[4m"
    if Theme.__strikethrough__ > 0:
        my_str += "\033[9m"
    if Theme.__outlined__ > 0:
        my_str += "\033[51m"
    if Theme.__inverted__ % 2 != 0:
        my_str += "\033[7m"
    bg = None
    fg = None
    for curr_theme in reversed(Theme.__applied_themes__):
        if bg is None and curr_theme.background_color is not None:
            bg = curr_theme.background_color
        if fg is None and curr_theme.foreground_color is not None:
            fg = curr_theme.foreground_color
        if fg is not None and bg is not None:
            break
    if bg is not None:
        my_color = None
        if isinstance(bg, str):
            my_color = Theme.__defined_colors__[bg]
        elif isinstance(bg, tuple):
            my_color = bg
        my_str += "\33[48;2;" + str(my_color[0]) + ";" + str(my_color[1]) + ";" + str(my_color[2]) + "m"
    if fg is not None:
        my_color = None
        if isinstance(fg, str):
            my_color = Theme.__defined_colors__[fg]
        elif isinstance(fg, tuple):
            my_color = fg
        my_str += "\33[38;2;" + str(my_color[0]) + ";" + str(my_color[1]) + ";" + str(my_color[2]) + "m"
    return my_str


def apply_theme(theme):
    my_theme = None
    if isinstance(theme, str):
        my_theme = Theme.themes[theme]
    else:
        my_theme = theme
    Theme.__applied_themes__.append(my_theme)
    if my_theme.bold:
        Theme.__bold__ += 1
    if my_theme.italic:
        Theme.__italic__ += 1
    if my_theme.underlined:
        Theme.__underlined__ += 1
    if my_theme.strikethrough:
        Theme.__strikethrough__ += 1
    if my_theme.outlined:
        Theme.__outlined__ += 1
    if my_theme.inverted:
        Theme.__inverted__ += 1
    if not Theme.__bypass_call__:
        print(__current_formatting__())


def pop_theme():
    if len(Theme.__applied_themes__) > 0:
        my_theme = Theme.__applied_themes__.pop()
        if my_theme.bold:
            Theme.__bold__ -= 1
        if my_theme.italic:
            Theme.__italic__ -= 1
        if my_theme.underlined:
            Theme.__underlined__ -= 1
        if my_theme.strikethrough:
            Theme.__strikethrough__ -= 1
        if my_theme.outlined:
            Theme.__outlined__ -= 1
        if my_theme.inverted:
            Theme.__inverted__ -= 1
        if not Theme.__bypass_call__:
            print(__current_formatting__())


def themed(theme, my_text):
    my_str = ""
    my_theme = None
    if isinstance(my_theme, str):
        my_theme = Theme.themes[theme]
    else:
        my_theme = theme
    Theme.__bypass_call__ = True
    apply_theme(my_theme)
    my_str = __current_formatting__()
    pop_theme()
    Theme.__bypass_call__ = False
    return my_str + my_text + __current_formatting__()


class Menu:

    def __init__(self, title, menu_items, exit_value, *, invalid_return_value=-1):
        self.title = title
        self.menu_items = menu_items
        self.exit_value = exit_value
        self.invalid_return_value = invalid_return_value
        self.__message_theme__ = None

    def show(self, *, message=None, center_message=False, prompt=None, indent=0, message_style=None, error=False, information=False):
        for i in range(100):
            print()
        indent_str = ""
        if indent > 0:
            for i in range(indent):
                indent_str += '\t'
        menu_width = len(self.title)
        message_lines = list()
        keys = list(self.menu_items.keys())
        keys.sort()
        max_key_length = 0
        max_menu_item_length = 0
        theme = None
        if message is not None:
            if error:
                theme = Theme.themes["Error Message"]
            elif information:
                theme = Theme.themes["Info Message"]
            elif message_style is not None:
                theme = message_style
            else:
                theme = self.__message_theme__
            for line in message.replace('\r', "").split('\n'):
                message_lines.append(line)
                if len(line) > menu_width:
                    menu_width = len(line)
        for key in keys:
            if len(str(key)) > max_key_length:
                max_key_length = len(str(key))
            if len(self.menu_items[key]) > max_menu_item_length:
                max_menu_item_length = len(self.menu_items[key])
        if max_key_length + max_menu_item_length + 1 > menu_width:
            menu_width = max_key_length + max_menu_item_length + 1
        print(indent_str + "╭" + "".rjust(menu_width + 2, "─") + "╮")
        if message is not None:
            for line in message_lines:
                result = line.center(menu_width) if center_message else line.ljust(menu_width)
                result = ' ' + result + ' '
                if theme is not None:
                    print(indent_str + "│" + themed(theme, result) + "│")
                else:
                    print(indent_str + "│" + result + "│")
        print(indent_str + "│" + "".ljust(menu_width + 2, "▒") + "│")
        print(indent_str + "│ " + self.title.center(menu_width) + " │")
        print(indent_str + "├" + "".ljust(menu_width + 2, "─") + "┤")
        for key in keys:
            print(indent_str + "│ " + (str(key).rjust(max_key_length) + " " + self.menu_items[key]).ljust(
                menu_width) + " │")
        print(indent_str + "╰" + "".rjust(menu_width + 2, "─") + "╯")

        if prompt is not None:
            response = input(indent_str + prompt)
            if response in self.menu_items.keys():
                return response
            else:
                response = response.upper()
                for key in self.menu_items.keys():
                    if response == str(key).upper():
                        return key
                try:
                    response = int(response)
                    for key in self.menu_items.keys():
                        if response == int(key):
                            return int(key)
                    return self.invalid_return_value
                except ValueError:
                    return self.invalid_return_value

    def set_theme(self, theme):
        self.__message_theme__ = theme


themes["Error Message"] = Theme(background_color=(255, 0, 0))
themes["Info Message"] = Theme(background_color=(0, 0, 255))
themes["Error"] = Theme(foreground_color=(255, 0, 0))
themes["Caution"] = Theme(foreground_color=(255, 215, 0))
themes["Underlined"] = Theme(underlined=True)
themes["Outlined"] = Theme(outlined=True)
themes["Orange"] = Theme(background_color=(255, 131, 0), foreground_color=(0, 0, 0))
