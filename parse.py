
def cluster(iterable, func=lambda x, y: x != y):
    """Take an iterable and yield groups according to a rule.

    The function is applied to each consecutive pair of items in the iterable
    in turn; when it returns true the accumulated group is yielded.
    """
    def next_or_none(iterable):
        try:
            return iterable.next()
        except StopIteration:
            return None

    group = []
    lookahead = next_or_none(iterable)
    while lookahead:
        token = lookahead
        lookahead = next_or_none(iterable)
        group.append(token)
        if func(token, lookahead):
            yield group
            group = []

if __name__ == "__main__":
    print list(cluster(iter([1,1,1,2,2,2])))
    print list(cluster(iter([1,1,1,2,2,2,1,1,1]), lambda x, y: x > y))
