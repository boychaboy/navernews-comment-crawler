import json
import os
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

AVAILABLE_KEYS = {"text", "corpus_source", "url", "domain", "title", "author", "html", "date", "misc"}


@dataclass
class Corpus:
    # 제목
    title: str
    # 문서 작성 날짜
    date: str
    corpus_source: str
    # 댓글 수
    num_comments : int
    # 댓글
    comments: Optional[List[str]] = None
    # 문서 URL
    url: Optional[str] = None
    # 기타 정보 (예: nsmc label)
    misc: Optional[Dict[str, Any]] = None

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)

    def dumps(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def loads(json_text: str) -> "Corpus":
        # scrapinghub 에서 dict 저장시에 "_type"이라는 키를 별도로 붙여서 아래 로직 필요
        corpus_dict = {key: value for key, value in json.loads(json_text).items() if key in AVAILABLE_KEYS}
        return Corpus(**corpus_dict)


def dump_corpus_list(corpus_list: List[Corpus], file_path: str):
    """코퍼스 리스트를 입력으로 받아 jsonl 형식으로 저장하는 함수

    :param corpus_list: 저장할 코퍼스 리스트
    :type corpus_list: List[Corpus]
    :param file_path: jsonl 을 저장할 경로
    :type file_path: str
    """

    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".jsonl" and file_extension != ".jl":
        raise ValueError("corpus list 는 jsonl 형식으로만 저장이 가능합니다.")

    with open(file_path, "w") as f:
        for corpus in corpus_list:
            f.write(f"{corpus.dumps()}\n")


def load_corpus_list(file_path: str) -> List[Corpus]:
    """코퍼스가 저장된 jsonl 파일을 읽어서 코퍼스 객체들을 반환하는 함수

    :param file_path: 저장된 jsonl 경로
    :type file_path: str
    :return: 파일에서 읽은 코퍼스 리스트
    :rtype: List[Corpus]
    """

    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".jsonl" and file_extension != ".jl":
        raise ValueError("corpus list 는 jsonl 형식만 로드 가능합니다.")

    with open(file_path) as f:
        return [Corpus.loads(line.strip()) for line in f]


def replace_whitespace_char(text: str) -> str:
    """일부 Whitespace character(\\r, \\n, \\t)를 형태가 유지되도록 변환하는 함수

    :param text: 원본 문자열
    :type text: str
    :return 변환된 문자열
    :rtype: str
    """
    return text.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")


def revert_whitespace_char(text: str) -> str:
    """Whitespace character(\\r, \\n, \\t)가 변환된 문자열을 원본 문자열로 되돌리는 함수

    :param text: 변환된 문자열
    :type text: str
    :return 원본 문자열
    :rtype: str
    """
    return text.replace("\\r", "\r").replace("\\n", "\n").replace("\\t", "\t")


def dump_corpus_list_to_tsv(corpus_list: List[Corpus], file_path: str):
    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".tsv":
        raise ValueError("corpus list 는 tsv 형식으로만 저장이 가능합니다.")

    with open(file_path, "w") as f:
        f.write("제목\t소스\tURL\t도메인\t저자\t본문\tHTML\t작성날짜\t기타\n")
        for corpus in corpus_list:
            domain_str = ",".join(corpus.domain) if corpus.domain else ""

            title = replace_whitespace_char(corpus.title) if isinstance(corpus.title, str) else None
            author = replace_whitespace_char(corpus.author) if isinstance(corpus.author, str) else None
            text = replace_whitespace_char(corpus.text) if isinstance(corpus.text, str) else str(corpus.text)

            f.write(
                f"{title}\t"
                f"{corpus.corpus_source}\t"
                f"{corpus.url}\t"
                f"{domain_str}\t"
                f"{author}\t"
                f"{text}\t"
                f"{corpus.html}\t"
                f"{corpus.date}\t"
                f"{corpus.misc}\n"
            )


def load_corpus_list_from_tsv(file_path: str) -> List[Corpus]:
    _, file_extension = os.path.splitext(file_path)
    if file_extension != ".tsv":
        raise ValueError(".tsv 파일만 로딩 가능합니다.")

    corpus_list = []
    with open(file_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue

            splitted_line = line.strip().split("\t")
            title, corpus_source, url, domain_str, author, text, html, date, misc = (
                text for text in splitted_line if text is not None
            )
            domain = domain_str.split(",") if domain_str != "" else None

            title = revert_whitespace_char(title) if isinstance(title, str) else None
            author = revert_whitespace_char(author) if isinstance(author, str) else None
            text = revert_whitespace_char(text) if isinstance(text, str) else str(text)

            corpus = Corpus(text, corpus_source, url, domain, title, author, html, date, misc)
            corpus_list.append(corpus)

    return corpus_list

