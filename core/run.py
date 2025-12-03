import os

import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration from environment variables with defaults
host = os.environ.get("CORE_API_HOST", "0.0.0.0")
port = int(os.environ.get("CORE_API_PORT", "8000"))
debug = os.environ.get("CORE_API_DEBUG", "false").lower() == "true"
reload = os.environ.get("CORE_API_RELOAD", "true").lower() == "true"

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="debug" if debug else "info",
    )
