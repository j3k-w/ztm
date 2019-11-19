import requests
import argparse


class Bus():
    # def __init__(self, _stop):
    #     self.stop = self.get_stop(_stop)
    #     self.estimated_time = self.get_estimated_time()
    #     self.planned_time = self.get_planned_time()

    def json_from_api(self, _stop: int) -> dict:
        """Downloads the JSON of given bus line."""

        # Get the JSON
        _stop = 1212

        link = f'http://ckan2.multimediagdansk.pl/delays?stopId={_stop}'
        content = requests.get(link).json()

        # print(content['delay'][0]['estimatedTime'])

        for record in content['delay']:
            print(record)
            # print(record['estimatedTime'])

        return content


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stop", "-s",
                        help="STOP ID")
    args = parser.parse_args()

    bus = Bus()
    if not any(vars(args).values()):
        print("There are no arguments passed!")
    elif args.stop:
        bus.json_from_api(args.stop)
