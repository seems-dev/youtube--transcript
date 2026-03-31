from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from transcript import main
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],         # Allows specific origins
    allow_credentials=True,        # Allows cookies/auth headers to be sent
    allow_methods=["*"],           # Allows all methods (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"],           # Allows all headers
)
@app.get('/')
def root():
    return FileResponse("static/index.html")


@app.get("/transcript")
def stream_transcript(link: str):
    return StreamingResponse(
        main(link),
        media_type="text/event-stream",  # SSE media type
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )