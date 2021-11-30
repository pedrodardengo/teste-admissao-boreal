import os

import uvicorn

from src import main

if __name__ == "__main__":
    os.environ["DB_CONNECTION_STRING"] = "sqlite://"
    os.environ["TOKEN_SECRET"] = "AU890SU8903HU9FAU89as9783e783rfasdf9"
    uvicorn.run(
        f"{main.__name__}:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        workers=1,
        reload=True,
    )
