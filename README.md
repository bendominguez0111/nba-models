# NBA / Python betting challenge
This is the source code for an algorithm to allocate $1,000 towards NBA sports betting props. Regular updates on my twitter account <a target="_blank" href="https://www.twitter.com/bendominguez011">@bendominguez011</a>

## Project Requirements:

It's suggested you use Anaconda for PyMC3 and install the necessary g++ requirements.

`conda env create --file=environment.yml`

Add conda environment to Jupyter notebook:

`python -m ipykernel install --user --name=nba_betting_model`

You'll need to install `nba.api` seperately, and when you do, use the command:

`pip install nba.api --no-deps`

Python version: <= 3.10.5
Numpy version:  <= 1.21.5 (theanos in pymc3 requires less than 1.22.2, nba_api requires greater than 1.22.2, but the modules we'll use from the nba_api don't use numpy so it's fine)

To install Python dependencies:
`
pip install -r requirements.txt
`

### Environment variables
There's a couple environment variables that need to be set to be able to run the program. 
#### The Odds API
`ODDS_API_KEY`: Can retrieve your API key from this website here: https://the-odds-api.com/. There is a free version of the API, but it is limited to 500 requests/month. 

### PyMC3 on Windows
https://discourse.pymc.io/t/getting-a-working-pymc3-windows-10-installation-using-anaconda-an-installation-guide/8641
