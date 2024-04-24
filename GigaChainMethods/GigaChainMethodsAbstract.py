class GigaChainMethodsAbstract:
    # Get themes of the publication using gigachat, returns a dictionary where keys are the themes and values
    # are the evaluation made by the LLM about how prevalent that theme is
    def getThemes(self,
                  file_path: str) -> dict:
        pass
