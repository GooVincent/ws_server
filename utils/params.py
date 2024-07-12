import argparse


def parse_arguments(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8765)

    parsed_args = parser.parse_args(args)

    return parsed_args
