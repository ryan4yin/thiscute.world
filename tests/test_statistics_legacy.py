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


class LegacyStatisticsTest(unittest.TestCase):
    def test_data_conversion_import_does_not_require_analytics_client(self):
        self.assertTrue(callable(importlib.import_module("update_statistics").process_data))

    def test_legacy_and_current_posts_do_not_merge(self):
        process_data = importlib.import_module("update_statistics").process_data
        items = process_data(report([
            ("旧版标题", "/posts/linux-desktop-explained/", 6, 8, 180),
            ("新稿标题", "/posts/linux-desktop-architecture/", 7, 10, 210),
        ]))
        by_path = {row["pagePath"]: row for row in items}
        self.assertEqual(len(by_path), 2)
        self.assertEqual(by_path["/posts/linux-desktop-explained/"]["screenPageViews"], 8)
        self.assertTrue(by_path["/posts/linux-desktop-explained/"]["legacyPage"])
        self.assertNotIn("legacyPage", by_path["/posts/linux-desktop-architecture/"])

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
        self.assertNotIn("legacyPage", items[0])

    def test_legacy_without_trailing_slash_is_marked_in_both_row_orders(self):
        process_data = importlib.import_module("update_statistics").process_data
        paths = ["/posts/linux-desktop-explained", "/posts/linux-desktop-explained/"]
        for order in (paths, list(reversed(paths))):
            with self.subTest(paths=order):
                items = process_data(report([
                    ("旧稿", path, 6, 8, 180) for path in order
                ]))
                self.assertEqual(len(items), 1)
                self.assertEqual(items[0]["pagePath"], order[0])
                self.assertEqual(items[0]["screenPageViews"], 16)
                self.assertTrue(items[0]["legacyPage"])


if __name__ == "__main__":
    unittest.main()
