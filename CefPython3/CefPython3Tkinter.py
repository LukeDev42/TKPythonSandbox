from cefpython3 import cefpython as cef
import ctypes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from tkinter import ttk
from tkcalendar import Calendar, DateEntry

import sys
import os
import platform
import logging as _logging

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"


class MainFrame(tk.Frame):

    def __init__(self, root):
        self.browser_frame = None
        self.navigation_bar = None
        self.root = root

        # Root
        # root.geometry("900x640")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Tkinter example")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        #User options frame
        user_options_frame = tk.Frame(self)
        user_options_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.uo_start_date = DateEntry(user_options_frame, width=16, bd=2)
        self.uo_start_date.grid(row=1, column=0, padx=5, pady=5)
        uo_sd_label = ttk.Label(master=user_options_frame, text="Start Date", font=("Verdana", 10))
        uo_sd_label.grid(row=0, column=0, padx=5, pady=5)
        self.uo_end_date = DateEntry(user_options_frame, width=16, bd=2)
        self.uo_end_date.grid(row=1, column=1, padx=5, pady=5)
        uo_ed_label = ttk.Label(master=user_options_frame, text="End Date", font=("Verdana", 10))
        uo_ed_label.grid(row=0, column=1, padx=5, pady=5)

        self.uo_country_choice = tk.StringVar()
        countries = ["Canada", "Mexico", "USA"]
        uo_country_combobox = ttk.Combobox(user_options_frame, values=countries, textvariable=self.uo_country_choice,
                                           state="readonly")
        uo_country_combobox.grid(row=3, column=0, padx=5, pady=5)
        uo_cc_label = ttk.Label(user_options_frame, text="Country", font=("Verdana", 10))
        uo_cc_label.grid(row=2, column=0, padx=5, pady=5)
        self.uo_postal_code = tk.StringVar()
        uo_zip_entry = ttk.Entry(user_options_frame, width=15, textvariable=self.uo_postal_code)
        uo_zip_entry.grid(row=3, column=1, padx=5, pady=5)
        uo_ze_label = ttk.Label(user_options_frame, text="Postal Code", font=("Verdana", 10))
        uo_ze_label.grid(row=2, column=1, padx=5, pady=5)

        self.uo_weather_data_option = tk.StringVar(None, "Temperature")
        uo_weather_options_label = ttk.Label(user_options_frame, text="Weather Data Comparison", font=("Veranda", 10))
        uo_weather_options_label.grid(row=4, column=0, columnspan=2)
        uo_weather_options_radio1 = ttk.Radiobutton(user_options_frame, variable=self.uo_weather_data_option,
                                                    text="Temperature", value="Temperature")
        uo_weather_options_radio2 = ttk.Radiobutton(user_options_frame, variable=self.uo_weather_data_option,
                                                    text="Solar Energy", value="Solar Energy")
        uo_weather_options_radio3 = ttk.Radiobutton(user_options_frame, variable=self.uo_weather_data_option,
                                                    text="UV Index", value="UV Index")
        uo_weather_options_radio1.grid(row=5, column=0)
        uo_weather_options_radio2.grid(row=6, column=0)
        uo_weather_options_radio3.grid(row=7, column=0)

        uo_button = ttk.Button(user_options_frame, text="Update Data", command=self.printUserOptions)
        uo_button.grid(row=8, column=0, columnspan=2)

        # NavigationBar
        # self.navigation_bar = NavigationBar(self)
        # self.navigation_bar.grid(row=0, column=0,
        #                          sticky=(tk.N + tk.S + tk.E + tk.W))
        # tk.Grid.rowconfigure(self, 0, weight=0)
        # tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, self.navigation_bar)
        self.browser_frame.grid(row=0, column=1, sticky="nswe", columnspan=3, rowspan=2)
        # tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 2, weight=1)
        tk.Grid.columnconfigure(self, 3, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.rowconfigure(self, 2, weight=1)


        #Pareto chart Frame
        self.label = tk.Label(self, text="Pareto Chart Frame", font=("Verdana", 12))
        self.label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        #Weather chart frame
        self.label1 = tk.Label(self, text="Weather Chart Frame", font=("Verdana", 12))
        self.label1.grid(row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=3)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def printUserOptions(self):
        print("These are the values the user has input")
        print("Start Date: ", self.uo_start_date.get_date())
        print("End Date: ", self.uo_end_date.get_date())
        print("Country: ", self.uo_country_choice.get())
        print("Postal Code: ", self.uo_postal_code.get())
        print("Weather Data Comparison: ", self.uo_weather_data_option.get())

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
            self.browser_frame = None
        else:
            self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "tkinter" + IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)


class BrowserFrame(tk.Frame):

    def __init__(self, mainframe, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        # rect = [0, 0, 1000, 1000]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             # url="C:\\Users\\leite\\Desktop\\Repos\\TKPythonSandbox\\output.html")
                                             url="C:\\Users\\leite\\Desktop\\Repos\\TKPythonSandbox\\output.html")
        assert self.browser
        self.browser.SetClientHandler(LifespanHandler(self))
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if MAC:
            # Do not use self.winfo_id() on Mac, because of these issues:
            # 1. Window id sometimes has an invalid negative value (Issue #308).
            # 2. Even with valid window id it crashes during the call to NSView.setAutoresizingMask:
            #    https://github.com/cztomczak/cefpython/issues/309#issuecomment-661094466
            #
            # To fix it using PyObjC package to obtain window handle. If you change structure of windows then you
            # need to do modifications here as well.
            #
            # There is still one issue with this solution. Sometimes there is more than one window, for example when application
            # didn't close cleanly last time Python displays an NSAlert window asking whether to Reopen that window. In such
            # case app will crash and you will see in console:
            # > Fatal Python error: PyEval_RestoreThread: NULL tstate
            # > zsh: abort      python tkinter_.py
            # Error messages related to this: https://github.com/cztomczak/cefpython/issues/441
            #
            # There is yet another issue that might be related as well:
            # https://github.com/cztomczak/cefpython/issues/583

            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            logger.info("winfo_id={}".format(self.winfo_id()))
            # noinspection PyUnresolvedReferences
            content_view = objc.pyobjc_id(NSApp.windows()[-1].contentView())
            logger.info("content_view={}".format(content_view))
            return content_view
        elif self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("BrowserFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        logger.info("BrowserFrame.on_root_close")
        if self.browser:
            logger.debug("CloseBrowser")
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        else:
            logger.debug("tk.Frame.destroy")
            self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class LifespanHandler(object):

    def __init__(self, tkFrame):
        self.tkFrame = tkFrame

    def OnBeforeClose(self, browser, **_):
        logger.debug("LifespanHandler.OnBeforeClose")
        self.tkFrame.quit()


class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())


class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        logger.debug("FocusHandler.OnGotFocus")
        if LINUX:
            self.browser_frame.focus_set()


class NavigationBar(tk.Frame):

    def __init__(self, master):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")

        # Back button
        back_png = os.path.join(resources, "back" + IMAGE_EXT)
        if os.path.exists(back_png):
            self.back_image = tk.PhotoImage(file=back_png)
        self.back_button = tk.Button(self, image=self.back_image,
                                     command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward_png = os.path.join(resources, "forward" + IMAGE_EXT)
        if os.path.exists(forward_png):
            self.forward_image = tk.PhotoImage(file=forward_png)
        self.forward_button = tk.Button(self, image=self.forward_image,
                                        command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        # Reload button
        reload_png = os.path.join(resources, "reload" + IMAGE_EXT)
        if os.path.exists(reload_png):
            self.reload_image = tk.PhotoImage(file=reload_png)
        self.reload_button = tk.Button(self, image=self.reload_image,
                                       command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        self.url_entry.grid(row=0, column=3,
                            sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """For focus problems see Issue #255 and Issue #535. """
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)


class Tabs(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        # TODO: implement tabs


if __name__ == '__main__':
    # main()
    logger.setLevel(_logging.DEBUG)
    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info("CEF Python {ver}".format(ver=cef.__version__))
    logger.info("Python {ver} {arch}".format(
        ver=platform.python_version(), arch=platform.architecture()[0]))
    logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    root = tk.Tk()
    root.geometry("1350x1000")
    app = MainFrame(root)
    settings = {}
    if MAC:
        settings["external_message_pump"] = True
    cef.Initialize(settings=settings)
    app.mainloop()
    logger.debug("Main loop exited")
    cef.Shutdown()