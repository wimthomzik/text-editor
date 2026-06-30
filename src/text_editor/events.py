from dataclasses import dataclass

@dataclass(frozen=True)
class Char:
    char: str

@dataclass(frozen=True)
class Backspace: ...

@dataclass(frozen=True)
class Enter: ...

@dataclass(frozen=True)
class Quit: ...

Event = Char | Backspace | Enter | Quit