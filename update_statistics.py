"""
参考：https://pakstech.com/blog/hugo-popular-content/

Update Website Statistics, fetch data from Google Analytics Data API

service_account file:
- 生成随机密码，保存到 github action secrets 中，环境变量名称为 `SERVICE_ACCOUNT_DECRYPT_KEY`
- encrypt command: `gpg --symmetric --cipher-algo AES256 google-service-account.json`
- decrypt command: `gpg --quiet --batch --yes --decrypt --passphrase='$SERVICE_ACCOUNT_DECRYPT_KEY' --output google-service-account.json google-service-account.json.gpg`
"""

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json
from pathlib import Path
import datetime as dt

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
PROPERTY = 'properties/259164768'

SERVICE_ACCOUNT_FILE = './google-service-account.json'
OUTPUT_PATH = "./data/website_statistics.json"


def initialize_analyticsreporting():
    """Initializes an Analytics Data API service object.

    Returns:
      An authorized Analytics Data API service object.
    """
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # Build the service object.
    analytics = build('analyticsdata', 'v1beta', credentials=credentials)

    return analytics


def process_data(data):
    result = dict()
    empty = tuple()
    for it in data.get('rows', empty):
      page = dict()
      for i, dimension in enumerate(it.get('dimensionValues', empty)):
        key = data['dimensionHeaders'][i]['name']
        page[key] = dimension['value']
      
      for i, metric in enumerate(it.get('metricValues', empty)):
        key = data['metricHeaders'][i]['name']
        page[key] = metric['value']
      

      if 'pageTitle' in page:
        page['pageTitle'] = page['pageTitle']\
          .replace(" - Ryan4Yin's Space", "")\
          .replace(" - This Cute World", "")

        page_path = page['pagePath']
        if not page_path.startswith("/posts/") \
          or page_path == "/posts/"\
          or page_path.startswith("/posts/page/"):
          # 只记录 /posts/ 博文的访问数据
          continue

        # 对统计数据按 path 合并下
        if page_path not in result:
          result[page_path] = page
        else:
          for k, v in page.items():
            if not isinstance(v, int):  # 只有数据才需要合并，跳过字符串
              continue
            result['page_path'][k] += v
      else:
        # 没有 pageTitle，这里应该是处理的 totalTrendingPosts
        result[""] = page
  
    return list(result.values())


def get_report_this_month(analytics):
    """
    Args:
      analytics: An authorized Analytics Data API service object.
    """
    body = {
        'dateRanges': [{'startDate': "30daysAgo", 'endDate': "today"}],
        # dimensions and metrics list: https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
        'metrics': [
            {'name': 'activeUsers'},
            {'name': 'screenPageViews'},
            {'name': 'userEngagementDuration'},
        ],
        'dimensions': [
            {'name': 'pageTitle'},
            {'name': 'pagePath'},
        ],
        "metricFilter": {
            "filter": {
                # https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression#Filter
                "fieldName": "userEngagementDuration",
                "numericFilter": {
                    "operation": "GREATER_THAN_OR_EQUAL",
                    "value": {
                        "int64Value": "10",  # 阅读时间超过 10s
                    },
                },
            }
        },
        "orderBys": [{"desc": True, "metric": {"metricName": "userEngagementDuration"}}],
        # "limit": "15",
    }
    data = analytics.properties().runReport(property=PROPERTY, body=body).execute()
    return process_data(data)


def get_report_from_start(analytics):
    """
    Args:
      analytics: An authorized Analytics Data API service object.
    """
    body = {
        'dateRanges': [{'startDate': "2021-01-01", 'endDate': "today"}],
        # dimensions and metrics list: https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
        'metrics': [
            {'name': 'activeUsers'},
            {'name': 'screenPageViews'},
            {'name': 'userEngagementDuration'},
        ]
    }
    data = analytics.properties().runReport(property=PROPERTY, body=body).execute()
    return process_data(data)[0]


def main():
    analytics = initialize_analyticsreporting()
    trendingThisMonth = get_report_this_month(analytics)
    total = get_report_from_start(analytics)
    website_statistics = {
      "updateDate": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
      "total": total,
      "trendingThisMonth": trendingThisMonth,
    }
    Path("./data/website_statistics.json").write_text(
      json.dumps(website_statistics, ensure_ascii=False, indent=2)
    )


if __name__ == '__main__':
    main()
