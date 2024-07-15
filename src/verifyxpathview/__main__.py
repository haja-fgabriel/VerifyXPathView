import argparse
from .views.main_view import MainWindow


def parse_args():
    parser = argparse.ArgumentParser(
        description="Application for visualizing XPath satisfiability tests",
    )
    # parser.add_argument("xml_schema")
    # parser.add_argument("xpath", required=False)

    return parser.parse_args()


def run(args):
    wnd = MainWindow()
    wnd.show()

    pass


if __name__ == "__main__":
    args = parse_args()
    run(args)