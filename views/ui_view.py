from PySimpleGUI import ErrorElement
import PySimpleGUI as sg


class UIView:
    def __init__(self):
        self.window = None

    def show_error_message(self, error_message: str) -> None:
        error_message_exists = not isinstance(self.window.find_element(
            'error_message', silent_on_error=True), ErrorElement)
        if (self.window and error_message_exists):
            self.window.find_element(
                'error_message', silent_on_error=True).update(error_message, background_color='#f5254b')

    def show_message(self, message):
        sg.Popup(message, keep_on_top=True)

    def close(self):
        if (self.window):
            self.window.close()
