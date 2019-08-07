# coding=utf-8
"""
@author: pavel.zhang
@contact: 2399546312@qq.com
@time: 2019/1/21 15:14
@description:
"""
from scrapy import cmdline


def main():
    cmdline.execute('news_spider crawl huxiu'.split())


if __name__ == "__main__":
    main()
