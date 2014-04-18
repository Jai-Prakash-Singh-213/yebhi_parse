# Scrapy settings for yebhi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yebhi'

SPIDER_MODULES = ['yebhi.spiders']
NEWSPIDER_MODULE = 'yebhi.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yebhi (+http://www.yourdomain.com)'

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED  = False


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'yebhi.proxymiddle.ProxyMiddleware': 100,
}

