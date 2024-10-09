from .random import StrategyRandom
from .english_random import StrategyEnglishRandom
from .sleepy import StrategySleepy
from .think_right import StrategyThinkRight
from .expectimax import StrategyExpectimax
from .monte_carlo import (
    StrategyMCTSEasy,
    StrategyMCTSMedium,
    StrategyMCTSHard,
    StrategyMCTSVeryHard,
)


ALL_STRATEGIES = [
    StrategyRandom,
    StrategyEnglishRandom,
    StrategySleepy,
    StrategyThinkRight,
    StrategyExpectimax,
    StrategyMCTSEasy,
    StrategyMCTSMedium,
    StrategyMCTSHard,
    StrategyMCTSVeryHard,
]

STRATEGY_LOOKUP = {
    strategy.name: strategy for strategy in ALL_STRATEGIES
}
