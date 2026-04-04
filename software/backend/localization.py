LANGUAGE_PACKS = {
    "en": {
        "ready": "Ready",
        "language_changed": "Language changed",
        "mode": "Mode",
        "iso": "ISO",
        "aperture": "Aperture",
        "shutter": "Shutter",
    },
    "cs": {
        "ready": "Pripraveno",
        "language_changed": "Jazyk zmenen",
        "mode": "Rezim",
        "iso": "ISO",
        "aperture": "Clona",
        "shutter": "Zaverka",
    },
}


class LocalizationManager:
    def __init__(self, locale="en"):
        self.locale = locale if locale in LANGUAGE_PACKS else "en"

    def set_locale(self, locale):
        if locale in LANGUAGE_PACKS:
            self.locale = locale

    def text(self, key, fallback=None):
        pack = LANGUAGE_PACKS.get(self.locale, LANGUAGE_PACKS["en"])
        if key in pack:
            return pack[key]
        if fallback is not None:
            return fallback
        return key

    def available_locales(self):
        return tuple(LANGUAGE_PACKS.keys())
