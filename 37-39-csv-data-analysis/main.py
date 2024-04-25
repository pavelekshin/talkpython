import cProfile
import getdata


profiler = cProfile.Profile()
profiler.disable()


def print_data(data):
    print("Alcohol data statistic for 2015\n")

    profiler.enable()

    data.init()

    beer_servings = data.beer_servings()
    wine_servings = data.wine_servings()
    spirit_servings = data.spirit_servings()
    total_litres = data.total_litres()

    profiler.disable()

    for record in beer_servings[:10]:
        print(
            "Most beer using country is {} with {} litters".format(
                record.country, record.beer_servings
            )
        )
    print("\n")

    for record in wine_servings[:10]:
        print(
            "Most wine using country is {} with {} litters".format(
                record.country, record.wine_servings
            )
        )

    print("\n")
    for record in spirit_servings[:10]:
        print(
            "Less spirit using country is {} with {} litters".format(
                record.country, record.spirit_servings
            )
        )

    print("\n")
    for record in total_litres[:15]:
        print(
            "Less alcohol using country is {} with {} litters".format(
                record.country, record.total_litres_of_pure_alcohol
            )
        )


if __name__ == "__main__":
    for i in range(100):
        print_data(getdata)

    profiler.print_stats(sort="cumtime")
