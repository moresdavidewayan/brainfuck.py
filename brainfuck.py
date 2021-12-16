from argparse import ArgumentParser
import os

os_name: str = os.name
if os_name == 'nt':
    import msvcrt
else:
    import tty, sys, termios

def getch() -> str:
    if os_name == 'nt':
        return msvcrt.getch()
    else:
        fd: int = sys.stdin.fileno()
        try:
            tty.setraw(sys.stdin.fileno())
            ch: str = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, termios.tcgetattr(fd))
        return ch

class Interpreter:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.array: list[int] = [0]
        self.pointer: int = 0

    def parse(self) -> None:
        current: int = 0
        left_braces: list[int] = []
        while current < len(self.source):
            match self.source[current]:
                case '>':
                    self.pointer += 1
                    if self.pointer == len(self.array): self.array.append(0)
                case '<':
                    if self.pointer == 0: self.array = [0] + self.array
                    else: self.pointer -= 1
                case '+': self.array[self.pointer] += 1
                case '-': self.array[self.pointer] -= 1
                case '.': print(chr(self.array[self.pointer]), end='')
                case ',': self.array[self.pointer] = ord(getch())
                case '[':
                    if self.array[self.pointer] == 0:
                        n: int = len(left_braces) + 1
                        while n != len(left_braces) or self.source[current] != ']':
                            current += 1
                            if self.source[current] == '[': n += 1
                            elif self.source[current] == ']': n -= 1
                    else: left_braces.append(current)
                case ']':
                    if self.array[self.pointer] != 0: current = left_braces[-1]
                    else: left_braces.pop()
            current += 1

def main() -> None:
    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument('file_path', help='the path of the file you want to execute')
    args = arg_parser.parse_args()
    with open(args.file_path) as file: source: str = ''.join(file.readlines())
    interpreter: Interpreter = Interpreter(source)
    interpreter.parse()

if __name__ == '__main__': main()