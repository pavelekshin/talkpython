from collections import Counter, namedtuple
import csv
from typing import Generator
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

from data.folder import get_folder_path

# Variable	Definition
# page_id	The unique identifier for that characters page within the wikia
# name	The name of the character
# urlslug	The unique url within the wikia that takes you to the character
# ID	The identity status of the character (Secret Identity, Public identity, [on marvel only: No Dual Identity])
# ALIGN	If the character is Good, Bad or Neutral
# EYE	Eye color of the character
# HAIR	Hair color of the character
# SEX	Sex of the character (e.g. Male, Female, etc.)
# GSM	If the character is a gender or sexual minority (e.g. Homosexual characters, bisexual characters)
# ALIVE	If the character is alive or deceased
# APPEARANCES	The number of appareances of the character in comic books (as of Sep. 2, 2014. Number will become increasingly out of date as time goes on.)
# FIRST APPEARANCE	The month and year of the character's first appearance in a comic book, if available
# YEAR	The year of the character's first appearance in a comic book, if available

DATA = get_folder_path('marvel-wikia-data.csv')
Character = namedtuple('Character', 'pid name sid align eye hair sex gsm alive appearances first_year year')


def convert_csv_to_dict(csvdata: str = DATA) -> Generator[Character, None, None]:
    """write a function to parse marvel-wikia-data.csv, see
       should return a list of OrderedDicts or a list of Character namedtuples"""

    with open(csvdata) as csv_file:
        reader: csv.DictReader = csv.DictReader(csv_file)
        for row in reader:
            yield Character(
                pid=row['page_id'],
                name=row['name'].split('(')[0].strip(),
                sid=row['ID'],
                align=row['ALIGN'],
                eye=row['EYE'],
                hair=row['HAIR'],
                sex=row['SEX'],
                gsm=row['GSM'],
                alive=row['ALIVE'],
                appearances=row['APPEARANCES'] if row['APPEARANCES'] else 0,
                first_year=row['FIRST APPEARANCE'] if row['FIRST APPEARANCE'] else 0,
                year=row['YEAR'],
            )


data: list[Character] = list(convert_csv_to_dict())


def most_popular_characters(n=5):
    """get the most popular character by number of appearances
       accept an argument of n (int) of most popular characters
       to return (leave default of 5)"""
    sorted_data = sorted(data, key=lambda x: int(x.appearances), reverse=True)
    return [each.name for each in sorted_data][:n]


def max_and_min_years_new_characters() -> tuple[str, str]:
    """Get the year with most and least new characters introduced respectively,
       use either the 'FIRST APPEARANCE' or 'Year' column in the csv data, or
       the 'year' attribute of the namedtuple, return a tuple of
       (max_year, min_year)"""
    years = [each.year for each in data if each.year]
    cnt = Counter(years)
    max_year = cnt.most_common()[0][0]
    min_year = cnt.most_common()[-1][0]
    return max_year, min_year


def percentage_female():
    """Get the percentage of female characters, only look at male and female
       for total, ignore the rest, return a percentage rounded to 2 digits"""
    character_sex = [each.sex for each in data]
    cnt = Counter(character_sex)
    total = cnt['Male Characters'] + cnt['Female Characters']
    return round(cnt['Female Characters'] / total * 100, 2)


def gsm_char():
    """Return dictionary of not binary characters"""
    return {each.name: each.gsm for each in data if each.gsm != ''}


def good_vs_bad(sex) -> dict[str, int]:
    """Return a dictionary of bad vs good vs neutral characters.
       This function receives an arg 'sex' and should be validated
       to only receive 'male' or 'female' as valid inputs (should
       be case-insensitive, so could also pass it MALE)

       The expected result should be a following dict. The values are
       rounded (int) percentages (values made up here):

       expected = {'Bad Characters': 33,
                   'Good Characters': 33,
                   'Neutral Characters': 33}
    """
    if sex.lower() not in ('male', 'female'):
        raise ValueError

    characters = [each.align for each in data if sex.title() in each.sex]
    cnt = Counter(characters)
    total = (cnt['Bad Characters'] +
             cnt['Good Characters'] +
             cnt['Neutral Characters'])

    return {
        'Bad Characters': round((cnt['Bad Characters'] / total) * 100),
        'Good Characters': round((cnt['Good Characters'] / total) * 100),
        'Neutral Characters': round((cnt['Neutral Characters'] / total) * 100),
    }


def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')


if __name__ == '__main__':
    print(most_popular_characters())
    print(max_and_min_years_new_characters())
    print(percentage_female())
    print(good_vs_bad('female'))
    print(good_vs_bad('male'))

    df = pd.DataFrame(data)

    # bar plot
    fig = px.bar(
        df[df['gsm'].str.strip().astype(bool)],
        x='name',
        y='gsm',
        color='gsm',
        orientation='v',
    )

    fig.update_layout(
        title=dict(
            text="Marvel non binary hero orientation",
            font=dict(size=32,
                      color="Blue"),
            automargin=True,
            yref='paper'),
        autosize=True,
        title_x=0.5,
        title_y=0.5,
        xaxis=dict(
            title="Hero",
            title_font_size=50,
            title_font_color="green",
            type="category",
            # ticklen=7,
            # tickwidth=3,
            tickson="labels",
            ticks="outside",
            showticklabels=True,
        ),
        yaxis=dict(
            title="Orientation",
            title_font_size=50,
            title_font_color="green",
            categoryarray=[""],
            # categoryorder="array",
        ),
        font=dict(size=18, color="black"),
        legend=dict(
            # x=0,
            y=0.5,
            # bgcolor='rgba(255, 255, 255, 0)',
            # bordercolor='rgba(255, 255, 255, 0)'
        ),
        # barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    fig.update_traces(hoverinfo="all", hovertemplate="Значение: %{x}<br>Значение: %{y}")
    plotly.offline.plot(fig, auto_play=False, auto_open=False, filename='hero_gsm')

    # pie / sunburst plot
    df.loc[df['gsm'].str.len() == 0, 'gsm'] = 'Other'  # Represent only nonbinary gender
    df = df.loc[df['gsm'] != 'Other']
    df['cnt'] = df['gsm'].map(df['gsm'].value_counts())
    df["percent"] = df["cnt"] / df["cnt"]
    print_full(df.head())

    print_full(df.groupby("gsm", as_index=False)
               .agg(count=("gsm", "size"), heroes=("name", list), years=("year", list))
               .sort_values(["count", "gsm"], ascending=[0, 1]))

    # fig = px.pie(df, values='percent', names='gsm', title='GSM')
    fig = px.sunburst(df,
                      values="percent",
                      path=["gsm", "name"],
                      hover_data=["name", ],
                      color="cnt",
                      color_continuous_scale="mint",
                      # color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
                      # color_discrete_sequence=px.colors.sequential.Blugrn,
                      )
    fig.update_traces(hoverinfo="all", textinfo="value")
    plotly.offline.plot(fig, auto_play=False, auto_open=False, filename="hero_gsm_pie")

    # scatter plot
    df3 = df.groupby("gsm", as_index=False).agg(count=("gsm", "size"), heroes=("name", list),
                                                years=("year", list)).sort_values(["count", "gsm"], ascending=[0, 1])


    def f(x, y):
        return '<br>'.join(f"{h} {z}" for h, z in zip(x, y))


    df3["heroes_label"] = df3[["heroes", "years"]].apply(lambda x: f(*x), axis=1)

    fig = px.scatter(df3,
                     x="count",
                     y="gsm",
                     # custom_data=['heroes'],
                     size="count",
                     color="gsm",
                     hover_data=["heroes_label", "years"],
                     log_x=True, size_max=200,
                     )
    fig.update_traces(hoverinfo="all", hovertemplate="<br>".join([
        "count: %{x}",
        "genome: %{y}",
        "heroes:<br>%{customdata[0]}",
        "<extra></extra>"]))
    fig.update_layout(hoverlabel=dict(bgcolor="white",
                                      font=dict(size=12, family="Arial", color="black"),
                                      align="auto",
                                      namelength=10))
    fig.update_layout(hovermode="x")
    plotly.offline.plot(fig, auto_play=False, auto_open=False, filename="hero_gsm_scatter")
