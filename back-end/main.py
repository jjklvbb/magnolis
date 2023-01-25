import uvicorn
import os

from app import create_app


if __name__ == '__main__':
    uvicorn.run("main:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)),
                log_level="info", reload=True, reload_dirs=["app"])
else:
    app = create_app()
