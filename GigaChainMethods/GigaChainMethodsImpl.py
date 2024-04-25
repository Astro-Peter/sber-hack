from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter

from GigaChainMethods.GigaChainMethodsAbstract import GigaChainMethodsAbstract
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat


class GigaChainMethodsImpl(GigaChainMethodsAbstract):
    gigachat = None

    def __init__(self,
                 key: str):
        self.gigachat = GigaChat(model="GigaChat-Pro", scope='GIGACHAT_API_CORP', credentials=key,
                                 verify_ssl_certs=False)

    def get_themes(self,
                   text: str) -> dict:
        contents = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=500,
            length_function=len,
            is_separator_regex=False, ).split_text(text)

        docs = [Document(page_content=t) for t in contents]
        chain = load_summarize_chain(self.gigachat, chain_type="stuff")
        summary = chain.invoke(docs)
        messages = [SystemMessage(content='you are an expert at selecting the primary scientific themes in articles'),
                    HumanMessage(
                        content=f"Выпиши только названия разделов науки, затронутые в данном текста и расположи их в порядке "
                                f"убывания по важности в статье через запятые без точки в конце: {summary.get('output_text')}")]
        bullet_points = self.gigachat(messages).content.lower()
        if bullet_points[-1] == '.':
            print("why?")
            bullet_points = bullet_points[:-1]
        print(bullet_points)
        bullets = [bullet.rstrip().lstrip() for bullet in bullet_points.split(',')]
        answer = {}
        for i in range(len(bullets)):
            answer[bullets[i]] = len(bullets) - i
        return answer
