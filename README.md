# WeatherCrawler
爬取天气数据的爬虫，会抓取从今天之后的七天天气数据

运行之前，确保已经安装scrapy、mongodb


安装scrapy: <code>pip install scrapy</code>

# 运行爬虫
<code>scrapy crawl province_spider</code>

或者指定日志级别的方式启动：

<code>scrapy crawl province_spider --loglevel INFO</code>

会依次从各省、市、县爬取天气数据，存入数据库，最终的数据如下：
<pre><code>
weather> db.wea.findOne()
{
        "_id" : ObjectId("598c1a0efb64421dcc437c47"),
        "province" : "湖北",
        "city" : "武汉",
        "data" : [
                {
                        "wind_force" : "微风",
                        "max_tem" : "35",
                        "min_tem" : "27℃",
                        "wind_direction" : [
                                "无持续风向",
                                "无持续风向"
                        ],
                        "day" : "10日（今天）",
                        "desc" : "晴转多云"
                },
              ...
  }

</code></pre>
