DEFAULT_FUNCTION_ORDER = (
    "preview",
    "capture",
    "menu",
    "playback",
    "settings",
    "sleep",
)

DEFAULT_USER_MASKS = {
    "hide_menu": False,
    "hide_playback": False,
    "hide_advanced_settings": False,
    "show_hint_badges": True,
}


class CustomizationProfile:
    def __init__(self, function_order=None, user_masks=None):
        self.function_order = list(function_order or DEFAULT_FUNCTION_ORDER)
        self.user_masks = dict(DEFAULT_USER_MASKS)
        if user_masks:
            self.user_masks.update(user_masks)

    def set_order(self, function_order):
        self.function_order = list(function_order)

    def set_mask(self, mask_name, enabled):
        self.user_masks[mask_name] = bool(enabled)

    def is_visible(self, function_name):
        if function_name == "menu" and self.user_masks.get("hide_menu", False):
            return False
        if function_name == "playback" and self.user_masks.get("hide_playback", False):
            return False
        if function_name == "settings" and self.user_masks.get("hide_advanced_settings", False):
            return False
        return True

    def ordered_visible_functions(self):
        return [name for name in self.function_order if self.is_visible(name)]
