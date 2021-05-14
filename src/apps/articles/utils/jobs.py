# -*- coding: utf-8 -*-
import os
import asyncio
from datetime import datetime

import redisai as rai
from django.db.utils import IntegrityError

from src.apps.articles.utils.parser import Parser
from src.apps.articles.utils.tokenizer import Tokenizer
from src.apps.articles.models import Article


def get_article_id(link):
    end = len(link) - 1
    start = link[:end].rfind('/') + 1
    return link[start:end]


def get_article_content(content):
    for i in content[0].iter():
        if i.tag == 'pre':
            i.getparent().remove(i)
    text = ''.join(content[0].itertext()).replace('\n', ' ').replace('\r', ' ')
    return text


async def parse_article(link, parser):
    xpaths = ['//article/div[1]/h1/span', '//*[@id="post-content-body"]']
    parser_results = await parser.parse_page(link, xpaths)
    title, raw_content = parser_results
    clean_content = get_article_content(raw_content)
    article_dict = {
        'id_': get_article_id(link),
        'link': link,
        'title': title[0].text,
        'clean_content': clean_content,
        'raw_content': ''.join(raw_content[0].itertext()),
    }
    return article_dict


async def parse_articles():
    parser = Parser()
    xpath_list = ['.//a[@class="toggle-menu__item-link toggle-menu__item-link_pagination"]/text()']
    pages = (await parser.parse_page('https://habr.com/ru/top/', xpath_list))
    num_pages = int(pages[0][-1])
    article_links = list()
    for page in range(1, num_pages+1):
        url = f'https://habr.com/ru/top/page{page}/'
        xpath_list = ['/html/body/div[1]/div[3]/div/section/div[1]/div[3]/ul/li/article/h2/a/@href']
        article_links += (await parser.parse_page(url, xpath_list))[0]

    existing_links = Article.objects.filter(
        timestamp__date=datetime.utcnow().date()
    ).values_list('link', flat=True)

    new_links = [i for i in article_links if i not in existing_links]

    coroutines = list()
    async with asyncio.Semaphore(10):
        for link in new_links:
            coroutines.append(parse_article(link, parser))

        articles = list()
        for func in asyncio.as_completed(coroutines):
            articles.append(await func)
    return articles


def dump_articles(articles):
    rai_connection = rai.Client(host='localhost', port='6379')
    tokenizer = Tokenizer()
    for article_dict in articles:
        tokens_array = tokenizer.run([article_dict['clean_content']])
        rai_connection.tensorset("input", tokens_array)
        rai_connection.modelrun("bert", ["input"], ["output"])
        embedding = rai_connection.tensorget("output")[0].tolist()
        article = Article(
            link=article_dict['link'],
            title=article_dict['title'],
            content=article_dict['raw_content'],
            timestamp=datetime.utcnow(),
            embedding=embedding,
        )
        try:
            article.save()
        except IntegrityError:
            continue


def load_articles():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    loop = asyncio.new_event_loop()
    articles = loop.run_until_complete(parse_articles())
    loop.close()

    dump_articles(articles)
    print('job done')
