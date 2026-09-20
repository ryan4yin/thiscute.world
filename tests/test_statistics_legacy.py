import importlib
import unittest


def report(rows):
    return {
        "dimensionHeaders": [{"name": "pageTitle"}, {"name": "pagePath"}],
        "metricHeaders": [
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"},
        ],
        "rows": [
            {
                "dimensionValues": [{"value": title}, {"value": path}],
                "metricValues": [
                    {"value": str(users)},
                    {"value": str(views)},
                    {"value": str(seconds)},
                ],
            }
            for title, path, users, views, seconds in rows
        ],
    }


RETIRED_PATHS = (
    "/posts/linux-desktop-explained/",
    "/posts/linux-desktop-1-boot-security/",
    "/posts/linux-desktop-2-systemd-services/",
    "/posts/linux-desktop-3-session-graphics/",
    "/posts/linux-desktop-4-multimedia-input/",
    "/posts/linux-desktop-5-network/",
    "/posts/linux-desktop-6-shutdown-troubleshooting/",
)


class RetiredStatisticsTest(unittest.TestCase):
    def test_data_conversion_import_does_not_require_analytics_client(self):
        self.assertTrue(callable(importlib.import_module("update_statistics").process_data))

    def test_retired_posts_are_excluded_but_unpublished_path_is_unchanged(self):
        process_data = importlib.import_module("update_statistics").process_data
        items = process_data(report([
            ("旧版标题", "/posts/linux-desktop-explained/", 6, 8, 180),
            ("新稿标题", "/posts/linux-desktop-architecture/", 7, 10, 210),
        ]))
        by_path = {row["pagePath"]: row for row in items}
        self.assertEqual(set(by_path), {"/posts/linux-desktop-architecture/"})

    def test_existing_sql_path_remap_still_merges(self):
        process_data = importlib.import_module("update_statistics").process_data
        items = process_data(report([
            ("SQL 旧稿", "/posts/sql-basic/", 6, 8, 180),
            ("SQL 新稿", "/posts/sql-basics-1/", 7, 10, 210),
        ]))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["pagePath"], "/posts/sql-basics-1/")
        self.assertEqual(items[0]["screenPageViews"], 18)

    def test_total_metrics_without_a_page_path_are_preserved(self):
        process_data = importlib.import_module("update_statistics").process_data
        data = report([])
        data["dimensionHeaders"] = []
        data["rows"] = [{
            "dimensionValues": [],
            "metricValues": [
                {"value": "6"}, {"value": "8"}, {"value": "180"},
            ],
        }]
        items = process_data(data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["screenPageViews"], 8)

    def test_all_retired_paths_are_excluded_with_or_without_trailing_slash(self):
        process_data = importlib.import_module("update_statistics").process_data
        for path in RETIRED_PATHS:
            for candidate in (path, path.rstrip("/")):
                with self.subTest(path=candidate):
                    items = process_data(report([
                        ("已下架文章", candidate, 6, 8, 180),
                    ]))
                    self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
