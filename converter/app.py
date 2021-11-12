from argparse import ArgumentParser
import json

from event import Event
import helpers


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path input CSV")
    parser.add_argument("-o", "--output", required=True, help="Path to output JSON")
    args = parser.parse_args()

    input_path: str = args.input
    output_path: str = args.output

    with open(input_path, "r") as fin, open(output_path, "w") as fout:
        reader = helpers.get_csv_reader(csvfile=fin)
        output = []
        for row in reader:
            if not row:
                continue
            event = Event.from_cols(data=row)
            if not event:
                continue
            output += event.to_dicts()
        fout.write(json.dumps(output))


if __name__ == "__main__":
    main()
