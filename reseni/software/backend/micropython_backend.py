"""Lightweight MicroPython backend for the camera project.

This file keeps the performance-sensitive parts outside of MicroPython.
It is meant to run as a control layer for button handling, device state
management, settings updates, command routing to native firmware, and
simple localization support.
"""

try:
    from localization import LocalizationManager
except ImportError:
    LocalizationManager = None

try:
    from customization import CustomizationProfile
except ImportError:
    CustomizationProfile = None


MODE_PREVIEW = "preview"
MODE_MENU = "menu"
MODE_CAPTURE = "capture"
MODE_PLAYBACK = "playback"
MODE_SLEEP = "sleep"
MODE_ERROR = "error"


class SettingsStore:
    def __init__(self):
        self.iso = 200
        self.aperture = 2.8
        self.shutter_speed_us = 10000

    def as_dict(self):
        return {
            "iso": self.iso,
            "aperture": self.aperture,
            "shutter_speed_us": self.shutter_speed_us,
        }


class CommandBus:
    def __init__(self, transport):
        self.transport = transport

    def send(self, command_name, payload=None):
        if payload is None:
            payload = {}
        self.transport.send({"command": command_name, "payload": payload})


class MockCoreLink:
    def send(self, message):
        print("[core-link]", message)


class Backend:
    def __init__(self, command_bus, locale="en"):
        self.command_bus = command_bus
        self.settings = SettingsStore()
        self.mode = MODE_PREVIEW
        self.last_event = None
        self.localization = LocalizationManager(locale) if LocalizationManager else None
        self.customization = CustomizationProfile() if CustomizationProfile else None

    def set_language(self, locale):
        if self.localization is None:
            return
        self.localization.set_locale(locale)

    def text(self, key, fallback=None):
        if self.localization is None:
            return fallback if fallback is not None else key
        return self.localization.text(key, fallback)

    def handle_button(self, button_name):
        self.last_event = button_name

        if button_name == "shutter":
            self.mode = MODE_CAPTURE
            self.command_bus.send(
                "capture_photo",
                {"iso": self.settings.iso, "aperture": self.settings.aperture},
            )
            return

        if button_name == "power":
            self.mode = MODE_SLEEP
            self.command_bus.send("enter_sleep")
            return

        if button_name == "menu":
            self.mode = MODE_MENU
            self.command_bus.send("open_menu")
            return

        if button_name == "iso_up":
            self.settings.iso = self.settings.iso + 100
            self.command_bus.send("set_iso", {"value": self.settings.iso})
            return

        if button_name == "iso_down":
            next_value = self.settings.iso - 100
            if next_value < 100:
                next_value = 100
            self.settings.iso = next_value
            self.command_bus.send("set_iso", {"value": self.settings.iso})
            return

        if button_name == "aperture_up":
            self.settings.aperture = self.settings.aperture + 1.0
            self.command_bus.send("set_aperture", {"value": self.settings.aperture})
            return

        if button_name == "aperture_down":
            next_aperture = self.settings.aperture - 1.0
            if next_aperture < 1.8:
                next_aperture = 1.8
            self.settings.aperture = next_aperture
            self.command_bus.send("set_aperture", {"value": self.settings.aperture})
            return

        if button_name == "sleep":
            self.mode = MODE_SLEEP
            self.command_bus.send("enter_sleep")
            return

        self.mode = MODE_ERROR
        self.command_bus.send("unknown_button", {"button": button_name})

    def apply_mode(self, new_mode):
        self.mode = new_mode
        self.command_bus.send("set_mode", {"mode": new_mode})

    def status(self):
        return {
            "mode": self.mode,
            "last_event": self.last_event,
            "settings": self.settings.as_dict(),
        }

    def set_function_order(self, function_order):
        if self.customization is None:
            return
        self.customization.set_order(function_order)

    def set_mask(self, mask_name, enabled):
        if self.customization is None:
            return
        self.customization.set_mask(mask_name, enabled)

    def visible_functions(self):
        if self.customization is None:
            return ["preview", "capture", "menu", "playback", "settings", "sleep"]
        return self.customization.ordered_visible_functions()


class ButtonRouter:
    def __init__(self, backend):
        self.backend = backend

    def press(self, button_name):
        print("[input] button:", button_name)
        self.backend.handle_button(button_name)


class SimpleUiBridge:
    def __init__(self, backend):
        self.backend = backend

    def refresh(self):
        state = self.backend.status()
        print(
            "[ui] {mode_label}={mode} {iso_label}={iso} {aperture_label}={aperture} {shutter_label}={shutter}".format(
                mode_label=self.backend.text("mode", "mode"),
                mode=state["mode"],
                iso_label=self.backend.text("iso", "iso"),
                iso=state["settings"]["iso"],
                aperture_label=self.backend.text("aperture", "aperture"),
                aperture=state["settings"]["aperture"],
                shutter_label=self.backend.text("shutter", "shutter"),
                shutter=state["settings"]["shutter_speed_us"],
            )
        )

    def show_message(self, key):
        print("[ui]", self.backend.text(key, key))

    def render_menu(self):
        functions = self.backend.visible_functions()
        if not functions:
            print("[ui] menu is empty")
            return

        print("[ui] menu order:")
        for index, function_name in enumerate(functions, start=1):
            label = self.backend.text(function_name, function_name)
            print("[ui]  {index}. {label}".format(index=index, label=label))


def demo():
    core_link = MockCoreLink()
    bus = CommandBus(core_link)
    backend = Backend(bus, locale="cs")
    router = ButtonRouter(backend)
    ui = SimpleUiBridge(backend)

    ui.show_message("ready")
    ui.refresh()
    ui.render_menu()

    backend.set_function_order(["capture", "preview", "settings", "sleep", "menu", "playback"])
    backend.set_mask("hide_playback", True)
    backend.set_mask("hide_advanced_settings", True)
    ui.render_menu()

    router.press("iso_up")
    router.press("aperture_up")
    router.press("shutter")
    ui.refresh()
    backend.set_language("en")
    ui.show_message("language_changed")
    ui.refresh()
    router.press("power")
    ui.refresh()


if __name__ == "__main__":
    demo()