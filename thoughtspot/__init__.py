"""
ThoughtSpot API library
"""
from functools import partial
from operator import is_not

__release_year__ = 2020
__release_month__ = 8
__release_patch__ = 1
__release_candidate__ = 'public_demo_only'

__version__ = version = '.'.join(
    list(
        filter(
            partial(is_not, None),
            [
                str(__release_year__),
                str(__release_month__),
                str(__release_patch__),
                __release_candidate__
            ]
        )
    )
)
