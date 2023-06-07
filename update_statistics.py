"""
参考: https://pakstech.com/blog/hugo-popular-content/

Update Website Statistics, fetch data from Google Analytics Data API

service_account file:
- 生成随机密码，保存到 github action secrets 中，环境变量名称为 `SERVICE_ACCOUNT_DECRYPT_KEY`
  - 注意密码不要包含插值符号 `$`，否则插值时会出各种问题
- encrypt command: `gpg --symmetric --cipher-algo AES256 google-service-account.json`
- decrypt command: `gpg --quiet --batch --yes --decrypt --passphrase="$SERVICE_ACCOUNT_DECRYPT_KEY" --output google-service-account.json google-service-account.json.gpg`
"""

import json
from operator import itemgetter
import re
import datetime as dt
from pathlib import Path

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
PROPERTY = 'properties/259164768'  # my site's google analytics property

SERVICE_ACCOUNT_FILE = './google-service-account.json'
OUTPUT_PATH = "./data/website_statistics.json"

# 有些文章的 path 被修改过，这里使用新路径进行统计
modified_page_paths = {
    # 旧路径 => 新路径
    "/posts/common-kubernetes-errors-causes-and-solutions/": "/posts/kubernetes-common-errors-and-solutions/",
    "/posts/sql-basic/": "/posts/sql-basics-1/",
    "/posts/likenttt-2020-12-13-guangzhou-marathon/": "/posts/likenttt-2020-12-13-guangzhou-marathon-3_30_15/",
    "/posts/kubernetes-deployemnt-using-kubeadm/": "/posts/kubernetes-deployment-using-kubeadm/",

    # experience 拼写错误
    "/posts/expirence-of-argo-workflow/": "/posts/experience-of-argo-workflows/",
    "/posts/expirence-of-pulumi/": "/posts/experience-of-pulumi/",
    "/posts/expirence-of-vault/": "/posts/experience-of-vault/",
}

# 有些文章的标题有更新，这里使用最新的标题替换掉旧标题
modified_page_titles = {
    # 路径 => 标题
    "/posts/about-tls-cert/": "写给开发人员的实用密码学（八）—— 数字证书与 TLS 协议",
    "/posts/qemu-kvm-usage/": "QEMU/KVM 虚拟化环境的搭建与使用",
    "/posts/nixos-and-flake-basics/": "NixOS 与 Nix Flakes 新手入门",
}


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


def humanize_duration(seconds: int):
    duration = str(dt.timedelta(seconds=seconds))
    duration = re.sub(r"(\d+):(\d+):(\d+)", r"\1h \2m \3s",
                      duration)  # 1:22:33 => 1h22m33s
    duration = duration\
        .replace("0h ", "")\
        .replace("00m ", "")  # 0h00m17s => 17s

    return duration


def process_data(data):
    """
    转换下数据格式，补充些额外的属性

    Args: 示例 {
      "dimensionHeaders": [{ "name": "pageTitle" }, { "name": "pagePath" }],
      "metricHeaders": [
          { "name": "activeUsers", "type": "TYPE_INTEGER" },
          { "name": "screenPageViews", "type": "TYPE_INTEGER" },
          { "name": "userEngagementDuration", "type": "TYPE_SECONDS" }
      ],
      "rows": [
          {
          "dimensionValues": [
              {
              "value": "欧几里得算法求最大公约数(GCD)的数学原理 - Ryan4Yin's Space"
              },
              { "value": "/posts/mathematics-in-euclidean-gcd/" }
          ],
          "metricValues": [{ "value": "4" }, { "value": "4" }, { "value": "11" }]
          },
          {
          "dimensionValues": [
              { "value": "SQL 基础笔记（一） - Ryan4Yin's Space" },
              { "value": "/posts/sql-basic/" }
          ],
          "metricValues": [{ "value": "1" }, { "value": "1" }, { "value": "10" }]
          }
      ]
    }


    Return: 示例 [
      {
        "pageTitle": "使用 Istio 进行 JWT 身份验证（充当 API 网关）",
        "pagePath": "/posts/use-istio-for-jwt-auth/",
        "activeUsers": 14,
        "screenPageViews": 19,
        "userEngagementDuration": 2402,
        "readingDuration": 2402,
        "humanizedReadingDuration": "40m 02s",
        "readingDurationPerUser": 171,
        "humanizedReadingDurationPerUser": "02m 51s"
      },
      {
        "pageTitle": "Linux 中的虚拟网络接口",
        "pagePath": "/posts/linux-virtual-network-interfaces/",
        "activeUsers": 38,
        "screenPageViews": 42,
        "userEngagementDuration": 6381,
        "readingDuration": 6381,
        "humanizedReadingDuration": "1h 46m 21s",
        "readingDurationPerUser": 167,
        "humanizedReadingDurationPerUser": "02m 47s"
      }
    ]
    """
    result = dict()
    empty = tuple()
    for it in data.get('rows', empty):
        page = dict()
        for i, dimension in enumerate(it.get('dimensionValues', empty)):
            key = data['dimensionHeaders'][i]['name']
            page[key] = dimension['value']

        for i, metric in enumerate(it.get('metricValues', empty)):
            key = data['metricHeaders'][i]['name']
            value = metric['value']
            if isinstance(value, str) and value.isdecimal():
                value = int(value)  # 转下整数
            page[key] = value

        if 'pageTitle' in page:
            page['pageTitle'] = page['pageTitle']\
                .replace(" - Ryan4Yin's Space", "")\
                .replace(" - This Cute World", "")

            # 跳过 404 相关页面
            if page['pageTitle'] in (
                "404 页面没找到",
                "404 Page not Found"
            ):
                continue

            # 处理被修改过 pagePath 的文章，使用指定的 Path
            page_path = page['pagePath']
            if "#" in page_path:
                # 统一去掉末尾的段落 id
                page_path = page_path.split("#")[0]
            if not page_path.endswith("/"):
                # path 统一以 / 结尾
                page_path += "/"
            if page_path in modified_page_paths:
                page_path = modified_page_paths[page_path]  # 替换成新的 pagePath
                page['pagePath'] = page_path

            # 跳过 posts 列表页
            if page_path in ("/posts/", "/en/posts/") \
                    or page_path.startswith("/posts/page/") \
                    or page_path.startswith("/en/posts/page/"):
                continue

            if not page_path.startswith("/posts/") \
                    and not page_path.startswith("/en/posts/"):
                # 只记录各文章页的访问数据
                continue

            # 对统计数据按 path 合并下
            if page_path not in result:
                result[page_path] = page
            else:
                for k, v in page.items():
                    if isinstance(v, int):  # 只有数据才需要合并，跳过字符串
                        result[page_path][k] += v

            # 处理被修改过 pageTitle 的文章，使用指定的 Title
            for path, title in modified_page_titles.items():
                if path not in result:
                    continue
                result[path]['pageTitle'] = title
        else:
            # 没有 pageTitle，这里应该是处理的 totalTrendingPosts
            result[""] = page

    items = []
    for p in result.values():
        if "userEngagementDuration" not in p:
            continue
        reading_duration = int(p['userEngagementDuration'])
        p['readingDuration'] = reading_duration
        p['humanizedReadingDuration'] = humanize_duration(reading_duration)

        activateUsers = int(p['activeUsers'])
        # 人均阅读时长
        reading_duration_per_user = reading_duration // activateUsers
        p['readingDurationPerUser'] = reading_duration_per_user
        p['humanizedReadingDurationPerUser'] = humanize_duration(
            reading_duration_per_user)

        if activateUsers < 5 or reading_duration_per_user < 20:
            # 跳过人均阅读时常低于 20s 或阅读人数低于 5 的文章（文章的质量偏低或者受众偏小，没必要列出来）
            continue

        items.append(p)

    return sorted(items, key=itemgetter("readingDurationPerUser"), reverse=True)


def get_report_last_n_days(analytics, n: int):
    """
    Args:
      analytics: An authorized Analytics Data API service object.
      n: queyr data in last n days

    Return: 与 process_data 一致
    """
    body = {
        'dateRanges': [{'startDate': f"{n}daysAgo", 'endDate': "today"}],
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
                        "int64Value": "180",  # 文档的总阅读时长超过 3 mins
                    },
                },
            }
        },
        "orderBys": [  # 按本月总阅读时长降序排列
            {"desc": True, "metric": {"metricName": "userEngagementDuration"}}
        ],
        # "limit": "15",
    }
    data = analytics.properties().runReport(property=PROPERTY, body=body).execute()
    return process_data(data)


def get_report_from_start(analytics):
    """
    Args:
      analytics: An authorized Analytics Data API service object.
    Return: {
        "activeUsers": 8292,
        "screenPageViews": 18145,
        "userEngagementDuration": 839453,
        "readingDuration": 839453,
        "humanizedReadingDuration": "9 days, 17h 10m 53s",
        "readingDurationPerUser": 101,
        "humanizedReadingDurationPerUser": "01m 41s"
      }

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


def get_shanghai_datetime_str():
    """
    获取到东八区的时间字符串

    Return:  2022-02-10T00:48UTC+08:00
    """
    tz_shanghai = dt.timezone(dt.timedelta(hours=8))
    now_shanghai = dt.datetime.now(tz=tz_shanghai)
    # 2022-02-10T00:48:52UTC+08:00
    return now_shanghai.strftime('%Y-%m-%dT%H:%M%Z')


def main():
    analytics = initialize_analyticsreporting()
    trendingThisMonth = get_report_last_n_days(analytics, n=90)
    total = get_report_from_start(analytics)

    website_statistics = {
        "updateDate": get_shanghai_datetime_str(),
        "total": total,
        "trendingThisMonth": trendingThisMonth,
    }
    Path("./data/website_statistics.json").write_text(
        json.dumps(website_statistics, ensure_ascii=False, indent=2)
    )


if __name__ == '__main__':
    main()
