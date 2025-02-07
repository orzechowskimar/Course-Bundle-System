from typing import Dict, List

from execptions import ProviderDataError, QuoteCalculationError
from logger import logger


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
        try:
            if "provider_topics" not in provider_data:
                raise ProviderDataError("Missing 'provider_topics' key in provider data.")
            providers = [
                Provider(name, topics.split("+"))
                for name, topics in provider_data["provider_topics"].items()
            ]
            logger.debug(f"Parsed {len(providers)} providers from provider data")
            return providers
        except Exception as e:
            logger.exception("Error parsing provider topics.")
            raise ProviderDataError(f"Invalid provider data: {e}")

    def __get_top_topics(self) -> List[tuple]:
        try:
            top_topics = sorted(self.__request["topics"].items(), key=lambda x: x[1], reverse=True)[:3]
            logger.info(f"Top topics determined: {top_topics}")
            return top_topics
        except KeyError as e:
            logger.error(f"Missing expected key in request data: {e}")
            raise

    def __calculate_quote(self, provider: Provider, top_topics: Dict[str, int]) -> float:
        try:
            matches = [topic for topic in provider.topics if topic in top_topics]
            logger.debug(f"Provider '{provider.name}' matches topics: {matches}")

            if len(matches) == 2:
                return 0.1 * sum(top_topics[topic] for topic in matches)
            elif len(matches) == 1:
                topic = matches[0]
                rank = list(top_topics.keys()).index(topic) + 1
                weight = {1: 0.2, 2: 0.25, 3: 0.3}.get(rank, 0)
                return weight * top_topics[topic]
            return 0
        except Exception as e:
            logger.exception(f"Error calculating quote for provider {provider.name}.")
            raise QuoteCalculationError(f"Failed to calculate quote for provider {provider.name}: {e}")

    def calculate_quotes(self) -> Dict[str, float]:
        top_topics = {k: v for k, v in self.__get_top_topics()}
        quotes = {
            provider.name: round(self.__calculate_quote(provider, top_topics), 2)
            for provider in self.__providers
        }
        final_quotes = {name: quote for name, quote in quotes.items() if quote > 0}
        logger.info(f"Final quotes: {final_quotes}")
        return final_quotes
