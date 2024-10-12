from pynput import keyboard
from threading import Thread


class HotkeyManager:
    def __init__(self):
        self.hotkeys = {}
        self.listener = None
        self.running = False

    def add_hotkey(self, key_combination, callback):
        """Add a hotkey with its associated callback function."""
        self.hotkeys[self._normalize_key(key_combination)] = callback

    def start(self):
        """Start listening for hotkeys."""
        if not self.running:
            self.running = True
            self.listener = keyboard.Listener(on_press=self._on_press)
            self.listener.start()

    def stop(self):
        """Stop listening for hotkeys."""
        if self.running:
            self.running = False
            if self.listener:
                self.listener.stop()

    def _on_press(self, key):
        """Internal method to handle key press events."""
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name

        normalized_key = self._normalize_key(key_name)
        if normalized_key in self.hotkeys:
            Thread(target=self.hotkeys[normalized_key]).start()

    def _normalize_key(self, key):
        """Normalize key representation."""
        return str(key).lower()

# Global instance of HotkeyManager
hotkey_manager = HotkeyManager()

def add_hotkey(key_combination, callback):
    """Add a hotkey with its associated callback function."""
    hotkey_manager.add_hotkey(key_combination, callback)

def start_listening():
    """Start listening for hotkeys."""
    hotkey_manager.start()

def stop_listening():
    """Stop listening for hotkeys."""
    hotkey_manager.stop()

# Example usage:
# add_hotkey('a', on_start)
# add_hotkey('s', on_stop)
# add_hotkey('k', hard_kill)
# start_listening()
# 
# # Your main loop here
# 
# stop_listening()  # When you're done
