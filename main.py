# In Powershell run: [    Set-ExecutionPolicy Unrestricted -Scope Process    ] before activating venv




from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

