import os
import sys
from flask import Flask, render_template
from cityiq import CityIq
import logging


log = logging.getLogger("my-logger")
app = Flask(__name__)


# token must be set as environmental variable
google_maps_token = os.getenv('GOOGLE_MAPS_TOKEN')
if not google_maps_token:
    log.error('GOOGLE_MAPS_TOKEN not set, exiting')
    sys.exit(-1)

# Get token used for all requests (does this time out?)
log.info('Getting cityIq token')
cityiq_client = CityIq("San Diego")
cityiq_client.fetchToken()


@app.route('/')
def traffic_map():
    cityiq_client.fetchMetadata("assets","traffic","eventTypes:TFEVT",page=0, size=10000)
    traffic_assets = cityiq_client.getAssets()
    log.info(f'Found {len(traffic_assets)} traffic assets')

    return render_template('google_map_w_markers.html', token=google_maps_token)
