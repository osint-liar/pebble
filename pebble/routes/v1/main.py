import logging
import os
import tempfile
from http.client import HTTPException
from typing import Dict, Any

import aiofiles
from fastapi import APIRouter
from starlette.datastructures import FormData
from starlette.requests import Request

from pebble.extractors.api_core_data_extractors import api_core_data_clone, api_core_data_convert_to_response
from pebble.extractors.ocr_extractors import pytesseract_ocr_command
from pebble.models.schemas.api_core_data_schema import ApiCoreDataSchemaV1, ApiCoreDataSchemaV1Response
from pebble.models.schemas.pebble_schema import PebbleResponseSchema

logger = logging.getLogger(__name__)
route = APIRouter()


@route.post('/upload')
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


def _commands(command_name: str) -> Any:
    """
    Helper function for mapping the given command to the given extractor function
    :param command_name:
    :return:
    """
    commands: Dict[str, Any] = {
        'pytesseract_ocr_command': pytesseract_ocr_command
    }
    if commands.get(command_name) is None:
        logger.error(f'Command {command_name} does not exist.')
        raise ValueError(f"No Command found for {command_name}")
    return commands.get(command_name)



