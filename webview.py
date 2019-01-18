import time
import threading
from typing import Callable

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, Gdk
from gi.repository import WebKit2

class MainWindow(Gtk.Window):

    ELEMENT_PADDING = 4

    PAGES = [
        ("Google", "http://google.com/", "", None, None),
        ("DuckDuckGo", "http://duckduckgo.com/", "", None, None),
        ("Yahoo", "http://yahoo.com/", "", None, None)
    ]

    # Load Config
    try:
        from config import PAGES
    except ImportError:
        pass
    try:
        from config import ELEMENT_PADDING
    except ImportError:
        pass

    def __init__(self):
        Gtk.Window.__init__(self, title="MP Kiosk Viewer")

        # Variable Setup
        self.renderer = []
        self.buttons = []

        # Loading Bar
        self.loading_bar = Gtk.ProgressBar()
        self.loading_bar.pulse()
        self.loading_bar.set_pulse_step(100)

        # Window Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root_box)
        root_box.pack_start(self._setup_toolbar(), False, False, MainWindow.ELEMENT_PADDING)
        root_box.pack_start(self.loading_bar, False, False, 0)
        root_box.pack_start(self._setup_webrenderer(), True, True, 0)

        # Window Setup
        self.connect("key-press-event",self._key_press_event)
        self.connect('destroy', Gtk.main_quit)
        self.fullscreen()
        self.show_all()

        # Select first
        self._load_tab_callback(0)(None)

    def _setup_toolbar(self) -> Gtk.Box:
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        for index, page in enumerate(MainWindow.PAGES):
            btn = Gtk.Button(label=page[0])
            btn.connect("clicked", self._load_tab_callback(index))
            self.buttons.append(btn)
            toolbar.pack_start(btn, False, False, MainWindow.ELEMENT_PADDING)

        self.btn_forward = Gtk.Button.new_from_icon_name('go-next', Gtk.IconSize.SMALL_TOOLBAR)
        self.btn_forward.set_sensitive(False)
        self.btn_forward.connect("clicked", self.go_forward)
        toolbar.pack_end(self.btn_forward, False, False, MainWindow.ELEMENT_PADDING)

        self.btn_reload = Gtk.Button.new_from_icon_name('view-refresh', Gtk.IconSize.SMALL_TOOLBAR)
        self.btn_reload.connect("clicked", self.refresh)
        toolbar.pack_end(self.btn_reload, False, False, MainWindow.ELEMENT_PADDING)

        self.btn_back = Gtk.Button.new_from_icon_name('go-previous', Gtk.IconSize.SMALL_TOOLBAR)
        self.btn_back.set_sensitive(False)
        self.btn_back.connect("clicked", self.go_back)
        toolbar.pack_end(self.btn_back, False, False, MainWindow.ELEMENT_PADDING)

        return toolbar

    def _setup_webrenderer(self) -> Gtk.Box:
        renderer_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        for page in MainWindow.PAGES:
            view = WebKit2.WebView()
            view.connect("authenticate", self._handle_http_auth_callback(page[3], page[4]))
            view.connect("load-changed", self._handle_load_changed)
            view.connect("load-changed", self._handle_load_change_callback(page[2]))
            view.connect("permission-request", self._handle_permission_request)
            view.get_settings().set_enable_media_stream(True)
            view.get_settings().set_enable_mediasource(True)
            view.get_settings().set_enable_webaudio(True)
            view.get_settings().set_enable_write_console_messages_to_stdout(True)
            view.load_uri(page[1])

            self.renderer.append(view)
            renderer_container.pack_start(view, True, True, 0)

        return renderer_container

    def _handle_http_auth_callback(self, username: str, password: str) -> Callable[[WebKit2.WebView, WebKit2.AuthenticationRequest], bool]:
        def func(web_view: WebKit2.WebView, auth_req: WebKit2.AuthenticationRequest) -> bool:
            if username is not None:
                auth_req.authenticate(WebKit2.Credential(username, password, WebKit2.CredentialPersistence.FOR_SESSION))
                return True
            return False
        return func

    def _key_press_event(self,widget,event) -> bool:
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        if ctrl and Gdk.keyval_name(event.keyval) == 'Tab':
            self._load_tab_callback((self.current_renderer_id + 1) % len(self.PAGES))(None)
            return True
        if ctrl and Gdk.keyval_name(event.keyval) == 'F5':
            self.current_renderer.reload_bypass_cache()
            return True
        if Gdk.keyval_name(event.keyval) == 'F5':
            self.current_renderer.reload()
            return True
        else:
            return False

    def _handle_load_change_callback(self, script: str = "") -> Callable[[WebKit2.WebView, WebKit2.LoadEvent], None]:
        def func(web_view: WebKit2.WebView, load_event: WebKit2.LoadEvent) -> None:
            if load_event is WebKit2.LoadEvent.FINISHED:
                web_view.run_javascript(script)
        return func

    def _handle_load_changed(self, web_view: WebKit2.WebView, load_event: WebKit2.LoadEvent) -> None:
        if web_view is not self.current_renderer:
            return

        if load_event is WebKit2.LoadEvent.STARTED:
            self.loading_bar.show()
        if load_event is WebKit2.LoadEvent.FINISHED:
            self.loading_bar.hide()
            self._button_update()

    def _handle_permission_request(self, web_view: WebKit2.WebView, request: WebKit2.PermissionRequest) -> bool:
        request.allow()
        return True

    def _load_tab_callback(self, id) -> Callable[[Gtk.Button], None]:
        def func(button: Gtk.Button) -> None:
            # Hide all renderers
            for renderer in self.renderer:
                renderer.hide()

            # Select id
            self.current_renderer_id = id
            self.current_renderer = self.renderer[id]
            self.current_renderer.show()
            self._button_update()
        return func

    def _button_update(self) -> None:
        for index, btn in enumerate(self.buttons):
            if index == self.current_renderer_id:
                btn.set_sensitive(False)
            else:
                btn.set_sensitive(True)

        self.btn_back.set_sensitive(self.current_renderer.can_go_back())
        self.btn_forward.set_sensitive(self.current_renderer.can_go_forward())

    def go_back(self, button: Gtk.Button) -> None:
        self.current_renderer.go_back()

    def refresh(self, button: Gtk.Button) -> None:
        self.current_renderer.reload()

    def go_forward(self, button: Gtk.Button) -> None:
        self.current_renderer.go_forward()


if __name__ == "__main__":
    t = MainWindow()
    Gtk.main()
