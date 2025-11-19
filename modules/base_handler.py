from abc import ABC, abstractmethod


class BaseHandler(ABC):

    def __init__(self, embedder, details_loader):
        self.embedder = embedder
        self.details_loader = details_loader

    @abstractmethod
    def get_content_type(self):
        pass

    @abstractmethod
    def format_result(self, result):
        pass

    @abstractmethod
    def get_system_prompt(self):
        pass

    def search(self, query, k=10, distance_threshold=0.8):
        # Search with embedder
        results = self.embedder.search(query, k=k)

        # Filter by distance
        filtered = [r for r in results if r['distance'] < distance_threshold]

        return filtered

    def enrich_result(self, result):
        row_id = result.get('رديف')
        if not row_id:
            return result

        # Get complete details
        if self.get_content_type() == 'book':
            details = self.details_loader.get_book_details(row_id)
        else:
            details = self.details_loader.get_thesis_details(row_id)

        if details:
            enriched = result.copy()
            enriched.update(details)
            return enriched

        return result

    def get_filters(self):
        return None  # Books don't have filters, theses override this
