import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from html import unescape
from typing import List
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


HACKER_NEWS_URL = "https://news.ycombinator.com/"


@dataclass
class NewsItem:
    rank: int
    title: str
    link: str


def fetch_html(url: str, timeout: int = 10) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
    )

    with urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_hacker_news(html: str, limit: int) -> List[NewsItem]:
    # HN 타이틀 링크: <span class="titleline"><a href="...">제목</a></span>
    pattern = re.compile(
        r'<span class="titleline"><a href="(?P<link>.*?)"[^>]*>(?P<title>.*?)</a></span>',
        re.IGNORECASE | re.DOTALL,
    )

    items: List[NewsItem] = []
    for idx, m in enumerate(pattern.finditer(html), start=1):
        title = re.sub(r"<.*?>", "", m.group("title"))
        title = unescape(title).strip()
        link = unescape(m.group("link")).strip()

        items.append(NewsItem(rank=idx, title=title, link=link))
        if len(items) >= limit:
            break

    return items


def print_items(items: List[NewsItem]) -> None:
    print("\n=== Hacker News Top Stories ===")
    for item in items:
        print(f"{item.rank:>2}. {item.title}")
        print(f"    {item.link}")


def save_json(items: List[NewsItem], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([asdict(item) for item in items], f, ensure_ascii=False, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="인터넷 정보를 스크래핑해서 출력하는 앱")
    parser.add_argument("--limit", type=int, default=10, help="출력할 뉴스 개수 (기본값: 10)")
    parser.add_argument("--output", type=str, help="결과를 저장할 JSON 파일 경로 (선택)")
    args = parser.parse_args()

    if args.limit <= 0:
        print("오류: --limit 값은 1 이상이어야 합니다.")
        return 1

    try:
        html = fetch_html(HACKER_NEWS_URL)
        items = parse_hacker_news(html, args.limit)
    except HTTPError as e:
        print(f"HTTP 오류 발생: {e}")
        return 1
    except URLError as e:
        print(f"네트워크 오류 발생: {e}")
        return 1
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        return 1

    if not items:
        print("스크래핑 결과가 없습니다. 페이지 구조가 변경되었을 수 있습니다.")
        return 1

    print_items(items)

    if args.output:
        save_json(items, args.output)
        print(f"\nJSON 파일 저장 완료: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
