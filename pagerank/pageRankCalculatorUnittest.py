import unittest
from pageRankCalculator import PageRank


class TestPageRank(unittest.TestCase):
    def setUp(self):
        self.links = {
            'page1': ['page2', 'page3'],
            'page2': ['page1'],
            'page3': ['page1', 'page2']
        }

    def test_initialize_page_ranks(self):
        pr = PageRank(self.links)
        pr.initialize_page_ranks()

        for page, page_rank in pr.page_ranks.items():
            self.assertEqual(page_rank, 1.0)

    def test_calculate_page_ranks(self):
        pr = PageRank(self.links)
        pr.initialize_page_ranks()
        pr.calculate_page_ranks()

        for page, page_rank in pr.page_ranks.items():
            self.assertTrue(page_rank >= 0.0)

    def test_get_page_ranks(self):
        pr = PageRank(self.links)
        pr.initialize_page_ranks()
        pr.calculate_page_ranks()

        self.assertEqual(pr.get_page_ranks(), pr.page_ranks)


if __name__ == '__main__':
    unittest.main()
