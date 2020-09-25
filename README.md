### What's this about?

* Create a new Python-based application (no framework is better, if you use a framework use Tornado or Falcon)

### Task 1
* Render the list of stores from the `stores.json` file in alphabetical order using a template.
* Use postcodes.io to get the latitude and longitude for each postcode. Render them next to each store location in the template.
* Build the functionality that allows you to return a list of stores in a given radius of a given postcode in the UK. The list must be ordered from north to south. No need to render anything, but the function needs to be unit tested.

### Task 2
* Build an API that returns stores from the `stores.json` file, based on a given search string and unit test it. For example, return "Newhaven" when searching for "hav". Make sure the search allows to use both city name and postcode.
* Order the results by matching postcode first and then matching city names. For example, "br" would have "Orpington" as the 1st result as its postcode is "BR5 3RP". Next would be "Bracknell", "Broadstairs", "Tunbridge_Wells", and "Brentford"
* Using your favourite frontend framework on the user-facing side:
  * Build a frontend that renders a text field for the query and the list of stores that match it
  * Add suggestions to the query field as you type, with a debounce effect of 100ms and a minimum of 2 characters
 

# Install

Use python3 <br />
Install dependencies
<br />
Helper script: `install.sh` or run `pip3 install -r requirements.txt`

# Run

gunicorn search:falcon_app
<br />
Open http://localhost:8000

# Comments
`boot.py` is just a sample file to run/debug <br />
`StoreRepository` is a `facade` and `repository` pattern. <br />
It does the sorting and finding via the helper classes.

The given radius part is usin the haversine distance.
<br />
The `nearest` endpoint from `postcodes.io` could have done
the same thing (almost) but I tried to use something local.
I think that was a trickier part. For the front-end, I just used vanilla JS 
because it's in the sense of `no frameworks`, lightweight.

For the HTTP server, I used falcon just to serve some http requests and avoid 
doing the same functionality from scratch.

## Instructions for Docker
cd /usr/src/watcher/watcherr/ <br />
docker build -t pyth3_docker . <br />
docker run -p 8000:8000 -it pyth3_docker  # Runs container interactively <br />
cd /usr/src/watcherr/watcherr #cd to app directory <br />
pip3 install -r requirements.txt #install requirements (only jinja2 was missing) <br />
gunicorn --bind 0.0.0.0:8000 search:falcon_app #(run gunicorn on all interfaces) <br />

Open http://localhost:8000 on host.