import sys
from pathlib import Path

from colorama import Fore, Style, init

init(autoreset=True)


def print_directory_contents(path, indentation=""):
    path = Path(path)
    
    if not path.exists():
        print(f"{path} does not exist")
        return
    
    if path.is_dir():
        print(f"{indentation}{Fore.BLUE}{Style.BRIGHT}{path.name}/")
        for item in sorted(path.iterdir()):
            print_directory_contents(item, indentation + "  ")
    else:
        print(f"{indentation}{Fore.GREEN}{path.name}")


def main():

    if len(sys.argv) < 2:
        print("Usage: python -m hw04.task3 <path_to_directory>")
        sys.exit(1)

    path = sys.argv[1]
    print_directory_contents(path)

    sys.exit(1)

    ...


if __name__ == "__main__":
    main()