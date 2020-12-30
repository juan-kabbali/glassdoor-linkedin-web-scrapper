# Glassdoor Linkedin Web Scrapper
CLI application that acts as web scrapper to retrieve Glassdoor and LinkedIn information

# How to use it
````shell script
scrapper-runner.py --help

Usage: scrapper-runner.py [OPTIONS]

Options:
  -c, --config-file TEXT  Path to config file
  -a, --analyse           Extract all information from scrapped files
  -C, --classify          Classify files from source web to landing zone
  -v, --verbose           Activate verbosity output
  -V, --version           Print current version and stops execution
  -t, --test              Dry run execution
  --help                  Show this message and exit.
````

### --classify
This flags allows to run the scrapper in classifier mode, it means that the scrapper will search all 
files from `dirs -> web_source` **env.yml** value, next it'll parse and move them to the correct dir
in the landing zone configured in `dirs -> landing_zone` **env.yml**

### --analyse
This flags allows to run the scrapper in analyser mode, it means that the scrapper will search all 
files from `dirs -> landing_zone` **env.yml** value, next it'll look inside each file for 
information about **enterprises**, **enterprises reviews** and **jobs** to create a **csv** file 
with semi-structured data.   

The analysed entities are enumerated in the **env.yml** file at `entities` propriety.

# How to install
1. Clone this repo ``git clone https://github.com/juan-kabbali/glassdoor-linkedin-web-scrapper.git``
2. Create a virtual environment with ``pipenv``
3. Install all dependencies ``pipenv install``
4. Lets scrap 🕷️🕸️

# Output example
If you want to know what kind of information this cli app can extract, you can go to 
the [docs folder](docs)
