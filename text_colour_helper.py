from colorama import Fore, Style


class TextColors:
    """Shortcuts for colorama colors to make console output easier to manage."""

    # Standard Colors
    R = Fore.RED
    G = Fore.GREEN
    B = Fore.BLUE
    Y = Fore.YELLOW
    C = Fore.CYAN
    M = Fore.MAGENTA
    W = Fore.WHITE
    BLK = Fore.BLACK

    # Light (Ex) Colors
    LR = Fore.LIGHTRED_EX
    LG = Fore.LIGHTGREEN_EX
    LB = Fore.LIGHTBLUE_EX
    LY = Fore.LIGHTYELLOW_EX
    LC = Fore.LIGHTCYAN_EX
    LM = Fore.LIGHTMAGENTA_EX
    LW = Fore.LIGHTWHITE_EX
    LBLK = Fore.LIGHTBLACK_EX

    # Text Styles
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM


# Create an instance for easy access
txt_clr = TextColors()
