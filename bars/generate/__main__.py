import json
import argparse
import bars.generate.main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan barcodes for playing music')

    parser = bars.generate.main.set_args()

    args = parser.parse_args()

    bars.generate.main.run(args)
