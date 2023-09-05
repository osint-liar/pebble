import uuid

import aiofiles
import uvicorn as uvicorn
from fastapi import FastAPI, Request, status, Body, File, UploadFile, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.middleware.cors import CORSMiddleware
from typing import List, Annotated
import logging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

from pebble.extractors.phone_extractors import phone_number_regex_extractor
from pebble.models.schemas.selector_schema import SelectorSchema
from pebble.extractors.email_extractors import email_by_regex
from pebble.models.schemas.enrichment_schema import EnrichmentSchema, MessageSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tags_metadata = [
    {
        "name": "pebble",
        "description": "Pebble is a simple FastApi service for use with OSINT LIAR.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

# set the origin to, chrome-extension://kblihpbdmlcmjbepgblpjdpllphhpfbk
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


@app.get("/")
def hello_world():
    return 'hello world'


@app.post('/extract-email-addresses')
async def extract_emails(text: str = Body(..., embed=True, alias='Text'), description="The raw data content.") -> EnrichmentSchema:
    selectors: List[SelectorSchema] = \
        [SelectorSchema(selector_name=email, selector_type_name='email') for email in email_by_regex(text)]
    message: MessageSchema = (
        MessageSchema(
            title='pebble Email Extract',
            message=f'There were {len(selectors)} found in the given text',
            type='success'))
    return EnrichmentSchema(selectors=selectors, message=message)


@app.post('/extract-phone-numbers')
async def extract_emails(text: str = Body(..., embed=True, alias='Text'), description="The raw data content.") -> EnrichmentSchema:
    selectors: List[SelectorSchema] = \
        [SelectorSchema(selector_name=phone_number, selector_type_name='phone') for phone_number in phone_number_regex_extractor(text)]
    message: MessageSchema = (
        MessageSchema(
            title='pebble Email Extract',
            message=f'There were {len(selectors)} found in the given text',
            type='success'))
    return EnrichmentSchema(selectors=selectors, message=message)


@app.post('/assign-tags')
async def assign_tags(text: str = Body(..., embed=True, alias='Text')) -> EnrichmentSchema:
    message: MessageSchema = (
        MessageSchema(
            title='pebble Tag Assignment',
            message=f'3 tags were assigned',
            type='success'))
    return EnrichmentSchema(tags=['Tag1', 'tag 2', 'tag ABC'], message=message)


@app.post('/assign-attributes')
async def assign_attributes(text: str = Body(..., embed=True, alias='Text')) -> EnrichmentSchema:
    message: MessageSchema = (
        MessageSchema(
            title='pebble Attribute Assignment',
            message=f'Attributes assigned',
            type='success'))
    return EnrichmentSchema(attributes=dict(project='pebble', product='osint_liar'), message=message)


@app.post('/upload')
async def upload_file(
    content_data: UploadFile = File(..., description="The raw data content.", alias='ContentData')
) -> EnrichmentSchema:
    file_path: str = f'/tmp/{uuid.uuid4()}'
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await content_data.read()  # async write chunk
        await out_file.write(content)
        out_file.close()
    message: MessageSchema = (
        MessageSchema(
            title='Pebble File Upload',
            message=f'File Uploaded',
            type='success'))
    return EnrichmentSchema(message=message)


@app.post("/html", response_class=HTMLResponse)
async def echo_html(html: str = Body(..., embed=True, alias='ContentHtml')) -> HTMLResponse:
    """
    Echo out the received html back.Demonstrates that you can build a custom html page response
    :param html:
    :return:
    """
    return html


if __name__ == "__main__":
    uvicorn.run("pebble.main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
