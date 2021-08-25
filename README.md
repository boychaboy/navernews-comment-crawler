[한국어](./README.md) | [English](./README_EN.md)

# Naver News Comment Crawler

본 크롤러는 네이버의 뉴스 기사, 날짜, 댓글(답글 포함)을 수집하는 크롤러입니다. 
`scrapy` 를 사용하여 작성하였습니다. 

## 설치

To install, follow these steps:

```
1. 구글 크롬을 설치합니다. 
2. 맞는 버전의 `chromedriver`를 [다운로드](https://chromedriver.chromium.org/downloads)한 다음 `./navernews-comment-crawler` 바로 아래로 이동합니다. 
3. `scrapy`, `selenium` 패키지를 설치합니다. 
```

## 크롤링

```
1. `scrapy crawl navernews -o {output_filename}
2. 뉴스를 검색할 "키워드"를 입력합니다. 
```

## Contact

If you want to contact me you can reach me at hoon2j@gmail.com
