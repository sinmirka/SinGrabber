from colorama import init, Style
from PIL.ImageColor import getcolor

init()

intro = """
███████╗██╗███╗   ██╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗      ██████╗██╗     ██╗
██╔════╝██║████╗  ██║    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║     ██║
███████╗██║██╔██╗ ██║    ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝    ██║     ██║     ██║
╚════██║██║██║╚██╗██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗    ██║     ██║     ██║
███████║██║██║ ╚████║    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║    ╚██████╗███████╗██║
╚══════╝╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚═════╝╚══════╝╚═╝
Welcome to SinGrabber CLI
Type "help" or "?" help
"""


def line_gradient(line, start_color, end_color):
    """Градиент для одной строки слева направо"""
    result = ""
    for i, char in enumerate(line):
        t = i / max(len(line) - 1, 1)
        r = int(start_color[0] * (1 - t) + end_color[0] * t)
        g = int(start_color[1] * (1 - t) + end_color[1] * t)
        b = int(start_color[2] * (1 - t) + end_color[2] * t)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    return result


def gradient(text, start_hex, end_hex):
    """Градиент по столбцам (слева → справа)"""
    start_color = getcolor(start_hex, "RGB")
    end_color = getcolor(end_hex, "RGB")

    lines = text.strip().split("\n")
    result = "\n"
    for line in lines:
        result += line_gradient(line, start_color, end_color) + "\n"

    return result + Style.RESET_ALL


gradient_intro = gradient(intro, start_hex="#6A82FB", end_hex="#FC5C7D")
