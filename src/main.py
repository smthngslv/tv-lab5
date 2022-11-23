import asyncio
from argparse import ArgumentParser

from lab5.queue import Producer, Consumer


async def main() -> None:
    # Add arguments. You will be able to launch different tasks with it.
    parser = ArgumentParser()
    parser.add_argument('--producer', action='store_true')
    parser.add_argument('--consumer', action='store_true')
    parser.add_argument('--count', action='store', type=int)
    args = parser.parse_args()

    if args.producer:
        print('Launching producer...', flush=True)

        if args.count is not None:
            print(f'Produce {args.count} messages...', flush=True)

        async with Producer() as producer:
            await producer.produce(count=args.count)

        return None

    if args.consumer:
        print('Launching consumer...', flush=True)

        async with Consumer() as consumer:
            await consumer.consume()

        return None

    parser.print_help()

if __name__ == '__main__':
    asyncio.run(main())
