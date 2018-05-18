import sys
from xmcuserimporter import Parser


def main():
    config_filename = sys.argv[1]
    csv_filename = sys.argv[2]

    Parser(config_filename, csv_filename).import_users()


if __name__ == "__main__":
    main()
