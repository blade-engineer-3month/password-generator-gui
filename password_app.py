import tkinter as tk
from tkinter import ttk
import secrets
import string
from dataclasses import dataclass, replace
from enum import Enum, auto


# パスワードオプションの定義
class OptionKey(Enum):
    UPPERCASE = auto()
    LOWERCASE = auto()
    DIGITS = auto()
    SYMBOLS = auto()
    LENGTH = auto()


@dataclass(frozen=True)
class PasswordOptions:
    uppercase: bool
    lowercase: bool
    digits: bool
    symbols: bool
    length: int

    def update(self, key: OptionKey, value: bool | int):
        match key:
            case OptionKey.UPPERCASE if isinstance(value, bool):
                return replace(self, uppercase=value)
            case OptionKey.LOWERCASE if isinstance(value, bool):
                return replace(self, lowercase=value)
            case OptionKey.DIGITS if isinstance(value, bool):
                return replace(self, digits=value)
            case OptionKey.SYMBOLS if isinstance(value, bool):
                return replace(self, symbols=value)
            case OptionKey.LENGTH if isinstance(value, int):
                return replace(self, length=value)
            case _:
                raise ValueError(f"Invalid option: {key}, {value}")


class PasswordGenerator:
    def __init__(self, options: PasswordOptions = None, custom_symbols: str = None):
        if options is None:
            options = PasswordOptions(
                uppercase=True, lowercase=True, digits=True, symbols=True, length=16
            )
        self.options = options
        self.custom_symbols = custom_symbols

    def generate(self):
        characters = ""
        password = []

        character_sets = [
            (self.options.uppercase, string.ascii_uppercase),
            (self.options.lowercase, string.ascii_lowercase),
            (self.options.digits, string.digits),
            (
                self.options.symbols,
                self.custom_symbols if self.custom_symbols is not None else string.punctuation,
            ),
        ]

        for enabled, character_set in character_sets:
            if enabled:
                characters += character_set
                password.append(secrets.choice(character_set))

        if not characters:
            raise ValueError("少なくとも1つの文字セットを有効にしてください")

        for _ in range(self.options.length - len(password)):
            password.append(secrets.choice(characters))

        secrets.SystemRandom().shuffle(password)
        return "".join(password)


# GUIアプリ
class PasswordApp:
    def __init__(self, root):
        self.root = root
        root.title("パスワード生成アプリ")

        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid()

        self.generate_button = ttk.Button(self.frame, text="実行", command=self.generate_passwords)
        self.generate_button.grid(row=0, column=0, columnspan=3, pady=10)

        self.labels = []
        self.entries = []
        self.copy_buttons = []

        for i, label_text in enumerate(["pw1", "pw2", "pw3", "pw4", "pw5"]):
            label = ttk.Label(self.frame, text=label_text)
            label.grid(row=i + 1, column=0, padx=5, pady=5, sticky="e")

            entry = ttk.Entry(self.frame, width=70)
            entry.grid(row=i + 1, column=1, padx=5, pady=5)

            copy_button = ttk.Button(self.frame, text="コピー", command=lambda e=entry: self.copy_to_clipboard(e))
            copy_button.grid(row=i + 1, column=2, padx=5, pady=5)

            self.labels.append(label)
            self.entries.append(entry)
            self.copy_buttons.append(copy_button)

    def generate_passwords(self):
        po1 = PasswordOptions(True, True, True, True, 32)
        po2 = PasswordOptions(False, False, True, True, 64)
        po3 = po2.update(OptionKey.SYMBOLS, False)
        po4 = PasswordOptions(True, True, True, True, 16)
        po5 = PasswordOptions(True, True, True, True, 126)

        pw1 = PasswordGenerator(po1).generate()
        pw2 = PasswordGenerator(po2).generate()
        pw3 = PasswordGenerator(po3).generate()
        pw4 = PasswordGenerator(po4).generate()
        pw5 = PasswordGenerator(po5, custom_symbols="@_").generate()

        passwords = [pw1, pw2, pw3, pw4, pw5]

        for entry, pw in zip(self.entries, passwords):
            entry.delete(0, tk.END)
            entry.insert(0, pw)

    def copy_to_clipboard(self, entry):
        pw = entry.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(pw)
        self.root.update()  # Clipboardに即時反映


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
