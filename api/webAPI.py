from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import logging
import os

from memberDB import get_member_by_token

load_dotenv()
log_file_path = os.getenv('LOG_FILE_PATH')
if log_file_path:
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%y-%m-%d %H:%M:%S',
    )
logging.getLogger("httpx").setLevel(logging.WARNING)

app = FastAPI(root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

@app.get("/")
def read_root():
    return {"Description": "Knights of Columbus Council 12172 Membership API v0.1"}

@app.get("/member/{token}")
def read_response(token: str):
    try:
        member = get_member_by_token(token)
    except Exception:
        raise HTTPException(status_code=404, detail="Token not valid")
    logging.info(f"Received token: {token} | Found member number: {member[0]}")
    return {"MemberNumber": member[0], "Name": f"{member[2]} {member[4]}"}

