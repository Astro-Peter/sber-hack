import io
import pypdf
import requests

from GoogleScholarMethods.GetRawText import GetRawText


class GetRawTextFromURL(GetRawText):
    def get_text(self,
                 url: str) -> str:
        response = requests.get(url)

        pdf_stream = io.BytesIO(response.content)
        pdf = pypdf.PdfReader(pdf_stream)

        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        return text
