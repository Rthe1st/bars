import json
import argparse
import bars.generate.main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan barcodes for playing music')
    
    with open('./config.json') as config_file:
        config = json.load(config_file)
    
    parser = bars.generate.main.set_args(config)

    args = parser.parse_args()

    bars.play.main.run(args, config)
