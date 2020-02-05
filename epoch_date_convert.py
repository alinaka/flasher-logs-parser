import argparse
import datetime


def get_datetime_from_seconds(seconds: int) -> datetime.timedelta:
    delta = datetime.timedelta(seconds=seconds)
    RS2_EPOCH = datetime.datetime(2018, 1, 1)
    return delta + RS2_EPOCH


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("seconds", type=int, help="epoch seconds of mfg date")
    args, _ = argparser.parse_known_args()
    print(get_datetime_from_seconds(seconds=args.seconds))


if __name__ == "__main__":
    main()
