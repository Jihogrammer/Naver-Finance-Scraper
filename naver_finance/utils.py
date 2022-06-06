from urllib.parse import quote


def parse_EUC_KR(value: str) -> str:
    """Naver 검색에서 사용되는 한글 인코딩 형식으로 변환합니다."""
    return quote(value, encoding="euc-kr")
