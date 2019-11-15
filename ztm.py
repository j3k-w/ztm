import requests
import json
import argparse
import contextlib

class Bus():
    def __init__(self):
        pass

    def json_from_api(self, title):
        """Downloads the JSON movie's data from API with given title."""

        # Get the JSON
        print(f"The '{title}' movie is being downloaded now...")
        link = f'http://www.omdbapi.com/?t={title}&apikey={self.API_KEY}'
        content = requests.get(link).json()

        # Pull the data from JSON
        columns = ['Year', 'Runtime', 'Genre', 'Director', 'Actors', 'Writer',
                   'Language', 'Country', 'Awards', 'imdbRating',
                   'imdbVotes', 'BoxOffice', 'Title']

        dt = []
        for col in columns:
            # Ben Hur case, when there is no BoxOffice column
            if col in content:
                dt.append(content[col])
            else:
                dt.append(None)
        return dt



def download():
    """Make a request and parse the returned value."""

    # couple of constans
    # n_szybowcowa = 1403
    n_pszenna = 7982

    now = datetime.now().time()
    now = "%d:%d" % (now.hour, now.minute)
    # print(now)

    r = requests.get(
        'http://ckan2.multimediagdansk.pl/delays?stopId=%d'
        % n_pszenna
    )
    # print("Status code: %d" % r.status_code)

    j = json.loads(r.text)

    if not j["delay"]:
        response = j["delay"][0]["theoreticalTime"]
    else:
        response = j["delay"][0]["estimatedTime"]

    print("The nearest bus will arrive at %s" % response)
    format = '%H:%M'
    time = datetime.strptime(response, format) - datetime.strptime(str(now), format)
    print(type(time))
    # time = timedelta.strftime(time)  # to fix, timedelta has no attribute strftime
    print("You've got", time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--download_all", action='store_true',
                        help="download all movies")
    parser.add_argument("--sort_by",
                        # nargs='+',
                        help="sort movies by columns")
    parser.add_argument("--filter_by",
                        nargs='+',
                        help="sort movies by columns")
    parser.add_argument("--compare",
                        nargs='+',
                        help="compare two movies by given value")
    parser.add_argument("--add", help="download and add a movie to the db")
    parser.add_argument("--highscores", action='store_true',
                        help="shows highscores in many categories")
    args = parser.parse_args()

    with contextlib.closing(DataLead(DB_NAME, API_KEY)) as DL:
        if not any(vars(args).values()):
            print("There are no arguments passed!")
        elif args.download_all:
            DL.download_all_movies()
        elif args.sort_by:
            DL.sort_by(args.sort_by)
        elif args.filter_by:
            DL.filter_by(args.filter_by)
        elif args.compare:
            DL.compare(args.compare)
        elif args.add:
            DL.add(args.add)
        elif args.highscores:
            DL.highscores(args.highscores)
