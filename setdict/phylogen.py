def main(species, scores):
    result = []
    while len(species) > 1:
        left, right = find_min_pair(species, scores)
        result.append(make_pair(left, right))
        species -= {left, right}
        make_new_pairs(species, scores, left, right)
        species.add(make_name(left, right))
    return result

def find_min_pair(species, scores):
    min_pair = None
    min_val = None
    for left in species:
        for right in species:
            if left < right:
                this_pair = make_pair(left, right)
                if (min_val is None) or (scores[this_pair] < min_val):
                    min_pair = this_pair
                    min_val = scores[this_pair]
    return min_pair

def make_new_pairs(species, scores, left, right):
    for current in species:
        left_score = scores[make_pair(current, left)]
        right_score = scores[make_pair(current, right)]
        new_score = (left_score + right_score) / 2.0
        scores[make_pair(current, make_name(left, right))] = new_score

def make_pair(left, right):
    if left < right:
        return (left, right)
    else:
        return (right, left)

def make_name(left, right):
    return '<%s, %s>' % make_pair(left, right)

if __name__ == '__main__':

    species = {'human', 'mermaid', 'werewolf', 'vampire'}

    scores = {
        ('human',   'mermaid')  : 12,
        ('human',   'vampire')  : 13,
        ('human',   'werewolf') :  5,
        ('mermaid', 'vampire')  : 15,
        ('mermaid', 'werewolf') : 29,
        ('vampire', 'werewolf') :  6
    }

    order = main(species, scores)
    print order
