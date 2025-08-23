import json
import sys
import os
from pathlib import Path

# Add the parent directories to sys.path to import our app
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.main import app
from mangum import Mangum

# Create the Mangum handler for AWS Lambda/Netlify Functions
handler = Mangum(app, lifespan="off")

def main(event, context):
    """
    Netlify Function handler for FastAPI app
    """
    try:
        # Handle the request through Mangum
        response = handler(event, context)
        return response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }
