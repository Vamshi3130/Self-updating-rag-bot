from fastapi import UploadFile
from docling.datamodel.base_models import InputFormat, DocumentStream
from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
)
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
import json
from io import BytesIO


class fileProcessingRepository:
    
    def __init__(self):
        pass 

    async def file_convert(self, file: UploadFile):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        #...

        ## Custom options are now defined per format.
        doc_converter = (
    DocumentConverter(  # all of the below is optional, has internal defaults.
        allowed_formats=[
            InputFormat.PDF,
            InputFormat.IMAGE,
            InputFormat.DOCX,
            InputFormat.HTML,
            InputFormat.PPTX,
        ],  # whitelist formats, non-matching files are ignored.
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, # pipeline options go here.
                backend=PyPdfiumDocumentBackend # optional: pick an alternative backend
            ),
            InputFormat.DOCX: WordFormatOption(
                pipeline_cls=SimplePipeline # default for office formats and HTML
            ),
        },
    )
        )
        content = await file.read()
        buf = BytesIO(content)
        stream = DocumentStream(name=file.filename,stream=buf)
        result = doc_converter.convert(stream).document.export_to_markdown()
        return result