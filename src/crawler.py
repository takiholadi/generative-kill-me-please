#!/usr/bin/env python3
import argparse
import dataclasses
import json
import pathlib
import logging
import random
import time
import typing as tp

import bs4
import requests


logging.basicConfig(filename='logs_crawler.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def download_html(url: str, timeout: int = 10) -> tp.Tuple[bool, str]:
    (is_sucess, html_page) = (False, '')
    try:
        response = requests.get(url, timeout=timeout)
        if response.ok:
            (is_sucess, html_page) = (True, response.text)
    except:
        pass
    return (is_sucess, html_page)


@dataclasses.dataclass
class Story:
    datetime: str
    tags: tp.List[str]
    text: str
    url: str
    votes: int


def html2story(html: str) -> Story:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    datetime = soup.find_all('div', attrs={'class': 'col-sm-6'})[0].text.strip()
    tags = ', '.join([x.strip() for x in soup.find_all('div', attrs={'class': 'col-sm-6'})[1].text.split(',')])
    text = soup.find_all('div', attrs={'class': 'col-xs-12'})[0].text.replace('\r', '\n').strip()
    url = 'https' + soup.find("meta", property="og:url")['content'].removeprefix('http')
    votes = int(soup.find_all('div', attrs={'class': 'col-xs-12'})[1].text.split('\n')[3])
    return Story(datetime=datetime, tags=tags, text=text, url=url, votes=votes)


class Crawler:

    def __init__(self, output_dirpath: str):
        self.output_dirpath = pathlib.Path(output_dirpath).resolve()
        self.urls = [f'https://killpls.me/story/{x}' for x in range(1, 30290 + 1)]

    def process(self) -> tp.List[str]:
        processed_filepaths = []
        for idx, each_url in enumerate(self.urls, 1):
            logger.info(f'Processing {idx}/{len(self.urls)} URL: {each_url}')
            output_json_filepath = (self.output_dirpath / pathlib.Path(each_url).stem).with_suffix('.json')
            processed_filepaths.append(output_json_filepath)
            is_already_downloaded = output_json_filepath.exists()
            if is_already_downloaded:
                logger.info(f'Already downloaded: {each_url}')
                continue
            time.sleep(random.uniform(0.4, 1.4))
            (is_sucess, html_page) = download_html(each_url)
            if not is_sucess:
                logger.warning(f'Problem downloading URL: {each_url}')
                continue
            try:
                story = html2story(html_page)
            except:
                logger.warning(f'Problem parsing URL: {each_url}')
            assert each_url == story.url
            self.output_dirpath.mkdir(parents=True, exist_ok=True)
            with open(output_json_filepath, 'w') as f:
                json.dump(dataclasses.asdict(story), f, ensure_ascii=False, indent=4)
            logger.info(f'Downloaded: {each_url}')
        return processed_filepaths


if __name__ == '__main__':
    logger.info('-=-=-=-=-=- START -=-=-=-=-=-')
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dirpath', type=str)
    args = parser.parse_args()
    crawler = Crawler(output_dirpath=args.output_dirpath)
    _ = crawler.process()
    logger.info('-=-=-=-=-=- END -=-=-=-=-=-')
