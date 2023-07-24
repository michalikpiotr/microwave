""" UI module"""
from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(tags=["UI"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main app"""
    return templates.TemplateResponse("index.html", {"request": request})
