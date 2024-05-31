# ECAN Riverflow API

This project provides an API to fetch riverflow observations from the ECAN Water Data API. It includes functionalities to fetch data on demand and serve it through a Flask application.

## Project Structure

- `app.py`: Main Flask application code.
- `meta.json`: Metadata file containing related metadata information.
- `observations.json`: Local observation data file used for initial data load (optional if you load data from the API).
- `fetch_observations.py`: Script to fetch observation data from the API and save it locally.
- `requirements.txt`: List of dependencies for the project.
- `wsgi.py`: WSGI entry point for Gunicorn.
- `update_observations.py`: Script to update observation data daily at midnight.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Peony8899/ECAN_Riverflow_api.git
    cd ECAN_Riverflow_api
    ```

2. Set up the virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Ensure your API key is correctly set in `fetch_observations.py`:
    ```python
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'your_api_key_here'
    }
    ```

## Usage

### Running the Flask Application

To run the Flask application, use the following command:
```bash
python app.py

Fetching Observation Data
You can fetch observation data by running:
python fetch_observations.py

This will save the fetched data to observations.json.

Updating Observations Daily
To automate the fetching of observations daily at midnight, you can set up a cron job. Add the following line to your crontab:
0 0 * * * /path/to/venv/bin/python /path/to/update_observations.py

API Endpoints
Get Metadata
Endpoint: /get_locations
Returns the metadata from meta.json.
Get Observations
Endpoint: /get_observations/YYYYMMDD
Fetches observation data for the specified date in the format YYYYMMDD. If the data is not available locally, it fetches it from the API and stores it locally.

Contributing
Feel free to submit issues or pull requests if you have any suggestions or improvements.

License
This project is licensed under the MIT License.

Save this content in a `README.md` file in the root directory of your project. This should provide a clear overview of your project, its structure, and how to use it.

