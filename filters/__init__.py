from filters.should_have_args import ShouldHaveArgs
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(ShouldHaveArgs)
