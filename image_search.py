from duckduckgo_search import DDGS


def search_duckduckgo_image(query: str) -> str:
    """
    用DuckDuckGo的非官方API搜索图片，返回第一个图片URL。
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            if results:
                return results[0]["image"]
    except Exception:
        pass
    return ""


search_duckduckgo_image("duck")
