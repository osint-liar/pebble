import os
import tempfile
import aiofiles
import uvicorn as uvicorn
from fastapi import FastAPI, Request, status, Body
from starlette.datastructures import FormData
from starlette.middleware.cors import CORSMiddleware
from typing import Dict, Any
import logging
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse
from pebble.extractors.api_core_data_extractors import api_core_data_clone, api_core_data_convert_to_response
from pebble.extractors.audio_to_text_extractors import whisper_extract_text_command
from pebble.extractors.ocr_extractors import pytesseract_ocr_command
from pebble.extractors.phone_extractors import phone_wrap
from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1
from pebble.models.schemas.pebble_schema import PebbleResponseSchema
from pebble.extractors.email_extractors import email_wrap

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tags_metadata = [
    {
        "name": "pebble",
        "description": "Pebble is a web service that provides access to a data engineering pipeline for OSINT LIAR.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

# to only allow connections from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.post('/v1/upload')
async def upload_file(request: Request) -> PebbleResponseSchema:
    def get_file_path(file_name: str) -> str:
        return os.path.join(tempfile.gettempdir(), file_name)

    form_data: FormData = await request.form()
    if form_data.get('ContentUuid') is None:
        raise HTTPException(status_code=400, detail="Field ContentUuid must be set")

    values = {k: v for k, v in form_data.items() if k != 'ContentData'}
    file_data = form_data['ContentData'].file.read()
    async with aiofiles.open(get_file_path(values['ContentUuid']), 'wb') as out_file:
        await out_file.write(file_data)
        # for now keep the binary data in memory
        values['ContentData'] = file_data
        # but also, keep the file path handy for the different extractors
        values['ContentFilePath'] = get_file_path(values['ContentUuid'])

    command_name = values['Cmd']
    cmd_func = _commands(command_name)
    del values['Cmd']
    if cmd_func is not None:
        parent = ApiCoreDataSchemaV1(**values)
        child = api_core_data_clone(parent)
        cmd_func(parent, child)
        child.content_title = f'Output from Pebble Api - {command_name}'
        return api_core_data_convert_to_response(child)
    return PebbleResponseSchema(Title='Error', Message='Invalid command', Type='error')


@app.post("/html", response_class=HTMLResponse)
async def echo_html(html: str = Body(..., embed=True, alias='ContentHtml')) -> HTMLResponse:
    """
    Echo out the received html back.Demonstrates that you can build a custom html page response
    :param html:
    :return:
    """
    return html


def _commands(command_name: str) -> Any:
    """
    Helper function for mapping the given command to the given extractor function
    :param command_name:
    :return:
    """
    commands: Dict[str, Any] = {
        'pytesseract_ocr_command': pytesseract_ocr_command,
        'email_extract': email_wrap,
        'phone_extract': phone_wrap,
        'whisper': whisper_extract_text_command
    }
    if commands.get(command_name) is None:
        logger.error(f'Command {command_name} does not exist.')
        raise HTTPException(status_code=400, detail=f'No Command found for {command_name}')
    return commands.get(command_name)

if __name__ == "__main__":
    uvicorn.run("pebble.main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
