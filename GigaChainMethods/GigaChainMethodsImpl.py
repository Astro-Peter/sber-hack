from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter

from GigaChainMethods.GigaChainMethodsAbstract import GigaChainMethodsAbstract
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models.gigachat import GigaChat


class GigaChainMethodsImpl(GigaChainMethodsAbstract):
    gigachat = None

    def __init__(self,
                 key: str):
        self.gigachat = GigaChat(model="GigaChat-Pro", scope='GIGACHAT_API_CORP', credentials=key,
                                 verify_ssl_certs=False)

    def getThemes(self,
                  text: str) -> dict:
        contents = RecursiveCharacterTextSplitter(
            chunk_size=7000,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,).split_text(text)

        docs = [Document(page_content=t) for t in contents]
        chain = load_summarize_chain(self.gigachat, chain_type="map_reduce")
        summary = chain.invoke(docs)
        messages = [SystemMessage(content='you are an expert at selecting the primary science spheres in articles'),
                    HumanMessage(
                        content=f"Напиши только научные сферы, затронутые в данном текста и расположи их в порядке "
                                f"убывания по важности в статье и напиши их через запятые без точки в конце: {summary}")]
        bullet_points = self.gigachat(messages).content.lower()
        bullets = [bullet.rstrip().lstrip() for bullet in bullet_points.split(',')]
        answer = {}
        for i in range(len(bullets)):
            answer[bullets[i]] = len(bullets) - i
        return answer
