class PageRank:
    def __init__(self, links):
        self.links = links
        self.page_ranks = {}

    def initialize_page_ranks(self):
        for page in self.links.keys():
            self.page_ranks[page] = 4.0

    def calculate_page_ranks(self, damping_factor=0.85, iterations=10):
        for _ in range(iterations):
            new_page_ranks = {}

            for page in self.links.keys():
                incoming_page_rank = 0.0
                for other_page, links in self.links.items():
                    if page in links:
                        incoming_page_rank += damping_factor * \
                            self.page_ranks[other_page] / len(links)

                new_page_rank = (1 - damping_factor) + incoming_page_rank
                new_page_ranks[page] = new_page_rank

            self.page_ranks = new_page_ranks

    def get_page_ranks(self):
        return self.page_ranks


links = {
    'A': ["B", "C"],
    'B': ['A', "C"],
    "C": []
}

page_rank_calculator = PageRank(links)
page_rank_calculator.initialize_page_ranks()
page_rank_calculator.calculate_page_ranks()

page_ranks = page_rank_calculator.get_page_ranks()
print("PageRanks:", page_ranks)
