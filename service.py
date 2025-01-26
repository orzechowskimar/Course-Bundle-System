from typing import Dict, List


class Provider:
    def __init__(self, name: str, topics: List[str]):
        self.__name = name
        self.__topics = topics

    @property
    def name(self) -> str:
        return self.__name

    @property
    def topics(self) -> List[str]:
        return self.__topics


class QuoteCalculator:
    def __init__(self, request: Dict, provider_data: Dict):
        self.__request = request
        self.__providers = self.__parse_provider_topics(provider_data)

    def __parse_provider_topics(self, provider_data: Dict) -> List[Provider]:
        return [
            Provider(name, topics.split("+"))
            for name, topics in provider_data["provider_topics"].items()
        ]

    def __get_top_topics(self) -> List[tuple]:
        return sorted(self.__request["topics"].items(), key=lambda x: x[1], reverse=True)[:3]

    def __calculate_quote(self, provider: Provider, top_topics: Dict[str, int]) -> float:
        matches = [topic for topic in provider.topics if topic in top_topics]

        if len(matches) == 2:
            return 0.1 * sum(top_topics[topic] for topic in matches)
        elif len(matches) == 1:
            topic = matches[0]
            rank = list(top_topics.keys()).index(topic) + 1
            weight = {1: 0.2, 2: 0.25, 3: 0.3}.get(rank, 0)
            return weight * top_topics[topic]
        return 0

    def calculate_quotes(self) -> Dict[str, float]:
        top_topics = {k: v for k, v in self.__get_top_topics()}
        quotes = {
            provider.name: round(self.__calculate_quote(provider, top_topics), 2)
            for provider in self.__providers
        }
        return {name: quote for name, quote in quotes.items() if quote > 0}
