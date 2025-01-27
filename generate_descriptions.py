from util import visual_description
from benchmark import *

BENCHMARK_TYPE = {
    'MMVet': 'FREE_FORM',
    'LLaVABench': 'FREE_FORM',
    'MMMU': 'MULTI_CHOICE',
    'ScienceQA': 'MULTI_CHOICE'
}

BENCHMARK_MAP = {
    'MMVet': MMVet,
    'LLaVABench': LLaVABench,
    'MMMU': MMMU,
    'ScienceQA': ScienceQA
}