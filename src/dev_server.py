import uvicorn
from dotenv import find_dotenv, load_dotenv

from src.main import app

load_dotenv(find_dotenv(".env"))

if __name__ == "__main__":
    app.openapi()
    uvicorn.run(
        f"{__name__}:app",
        host="0.0.0.0",
        port=7000,
        log_level="debug",
        workers=1,
        reload=True,
    )
