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
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, termios.tcgetattr(fd))
        return ch

class StackArray:
    def __init__(self) -> None:
        self.array: list[int] = [0]
        self.pointer: int = 0

    def set_pointer(self, position: int) -> None:
        self.pointer = position

    def get_value(self) -> int:
        return self.array[self.pointer]

    def move_right(self) -> None:
        self.pointer += 1
        if self.pointer == len(self.array):
            self.array.append(0)

    def move_left(self) -> None:
        if self.pointer == 0:
            self.array = [0] + self.array
        else:
            self.pointer -= 1
    
    def increment(self) -> None:
        self.array[self.pointer] += 1

    def decrement(self) -> None:
        self.array[self.pointer] -= 1

    def output(self) -> None:
        print(chr(self.array[self.pointer]), end='')

    def set(self) -> None:
        self.array[self.pointer] = ord(getch())

class Interpreter:
    def __init__(self, source: str) -> None:
        self.source: str = source
        self.stack_array: StackArray = StackArray()

    def parse(self) -> None:
        current: int = 0
        left_braces: list[int] = []
        while current < len(self.source):
            match self.source[current]:
                case '>':
                    self.stack_array.move_right()
                case '<':
                    self.stack_array.move_left()
                case '+':
                    self.stack_array.increment()
                case '-':
                    self.stack_array.decrement()
                case '.':
                    self.stack_array.output()
                case ',':
                    self.stack_array.set()
                case '[':
                    if self.stack_array.get_value() == 0:
                        n: int = len(left_braces) + 1
                        while n != len(left_braces) or self.source[current] != ']':
                            current += 1
                            if self.source[current] == '[':
                                n += 1
                            elif self.source[current] == ']':
                                n -= 1
                    else:
                        left_braces.append(current)
                case ']':
                    if self.stack_array.get_value() != 0:
                        current = left_braces[-1]
                    else:
                        left_braces.pop()
            current += 1

def main() -> None:
    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument('file_path', help='the path of the file you want to execute')
    args = arg_parser.parse_args()
    with open(args.file_path) as file:
        source: str = ''.join(file.readlines())
    interpreter: Interpreter = Interpreter(source)
    interpreter.parse()

if __name__ == '__main__':
    main()
