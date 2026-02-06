from argparse import ArgumentParser
import asyncio

from src.parser.parser import Parser


async def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--parse", type=str)
    args = argument_parser.parse_args()
    if args.parse:
        await Parser.parse(args.parse)
        return

    print("bot start")


if __name__ == "__main__":
    asyncio.run(main())
