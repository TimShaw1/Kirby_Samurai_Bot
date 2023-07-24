import win32.lib.win32con as win32con
import win32.win32gui as win32gui
import pyautogui
import ctypes
import copy
from PIL import Image
from typing import Union
import numpy

ctypes.windll.user32.SetProcessDPIAware()

def get_window_name() -> str:
    """
    Gets the full window name of yuzu (eg "yuzu Early Access 1234")

    Returns
    ----------
        str
            the name of the yuzu window
    """
    windows = pyautogui.getAllWindows()
    for w in windows:
        if "yuzu" in w.title:
            return w.title

def get_screenshot(dimensions: list[int] | None = None, window_title: str = get_window_name()) -> Image:
    """
    Gets a screenshot of the given window within the given dimensions

    Parameters
    ----------
        dimensions : tuple[int], optional
            the `[x, y, w, h]` dimensions of where to get the screenshot
        window_title : str, optional
            the title of the window

    Returns
    ----------
        im : Image
            the screenshot of the screen

    Raises
    ----------
        ValueError
            The window title was incorrect or the window was not open
    """
    if window_title:

        hwnd = win32gui.FindWindow(None, get_window_name())
        if hwnd and not dimensions:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        elif dimensions:
            im = pyautogui.screenshot(region=dimensions)
            return im
        else:
            raise ValueError("Window Not found")
    else:
        im = pyautogui.screenshot()
        return im
    
def get_game_screenshot(dim: list[int]) -> Image:
    """
    Returns a screenshot of the game section in Yuzu (window must be maximised)

    Parameters
    ----------
    dim : tuple[int]
        the `[x, y, w, h]` dimensions of where to get the screenshot

    Returns
    ----------
    screenshot : Image
        a screenshot of the screen

    Raises
    ----------
    AssertionError
        If the window is not maximised

    ValueError
        If yuzu is not open
    """
    window = win32gui.FindWindow(None, get_window_name())
    if window:
        tup = win32gui.GetWindowPlacement(window)
        if tup[1] == win32con.SW_SHOWMAXIMIZED:
            game_dim = copy.deepcopy(dim)
            game_dim[0] += round(dim[2] / 17.66)
            game_dim[1] += round(dim[3] / 20.05)
            game_dim[2] = round(dim[2] / 1.13)
            game_dim[3] = round(dim[3] / 1.05)

            return get_screenshot(game_dim)
        else:
            raise AssertionError("Window must be maximised")
    else:
        raise ValueError("Window Not found")
    
def get_dimensions(window_title: str = get_window_name()) -> list[int]:
    """
    Returns the `[x, y, w, h]` dimensions of the window
    
    Parameters
    ----------
    window_title: str, optional
        the name of the window

    Returns
    ----------
    tuple[int]
        the `[x, y, w, h]` dimensions of the window

    Raises
    ----------
    ValueError
        If window is not open or title is incorrect
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        return[x,y,x1,y1]
    else:
        raise ValueError("Window Not found")


def get_screen_coords() -> None:
    """
    Utility function that prints the current mouse position indefinitely
    """
    while True:
        print(pyautogui.position(), end='\r')

def get_screen_ratio(dim: list[int]) -> None:
    """
    Utility function that prints the current mouse position as a ratio indefinitely.
    - The ratio is `(window_width / (pos.x - window_x), window_height / (pos.y - window_y))` rounded to the nearest integer
    """
    while True:
        print(round(abs(dim[2] / (pyautogui.position().x - dim[0])), 2), round(abs(dim[3] / (pyautogui.position().y - dim[1])), 2), end='\r')

def get_max_pixel_diff(pixel: tuple[int], col: tuple[int]) -> int:
    """
    Utility function that gets the max difference between two colors
    """
    return max(abs(numpy.subtract(pixel, col)))