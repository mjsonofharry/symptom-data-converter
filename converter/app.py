from argparse import ArgumentParser
import dataclasses

from event import Event


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path input CSV")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON")
    args = parser.parse_args()

    input_path: str = args.input
    output_path: str = args.output

    with open(input_path, "r") as fin, open(output_path, "w") as fout:
        for row in fin.readlines():
            row = row.strip()
            if not row:
                continue
            print(row)
            event = Event.parse(data=row)
            if not event:
                continue
            # fout.write(event)
            # fout.write("\n")
            print(dataclasses.asdict(event))


if __name__ == "__main__":
    main()
