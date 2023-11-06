import itertools

scrabble_scores = [(1, "E A O I N R T L S U"), (2, "D G"), (3, "B C M P"),
                   (4, "F H V W Y"), (5, "K"), (8, "J X"), (10, "Q Z")]
LETTER_SCORES = {letter: score for score, letters in scrabble_scores
                 for letter in letters.split()}


def _get_permutations_draw(draw):
    draw = ''.join(draw).lower()
    print(draw)
    return [list(itertools.permutations(draw,i)) for i in reversed(range(2,len(draw)+1))]

a = _get_permutations_draw('T, I, I, G, T, T, L')
