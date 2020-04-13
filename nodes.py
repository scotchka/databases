def equals(x, y):
    return x == y


def contains(string, substring):
    return substring in string


BIN_OPS = {"EQUALS": equals, "CONTAINS": contains}


class Node:
    def __init__(self, *args, child=None):
        self.args = args
        self.child = child
        self.schema = None


class Filescan(Node):
    def __iter__(self):
        (path,) = self.args

        with open(path) as f:
            columns = next(f).strip().split(",")
            self.schema = dict(zip(columns, range(len(columns))))
            for line in f:
                yield tuple(line.strip().split(","))


class Selection(Node):
    def __iter__(self):
        column, op_name, value = self.args

        for row in self.child:
            if not self.schema:
                self.schema = self.child.schema
            if BIN_OPS[op_name](row[self.child.schema[column]], value):
                yield row


class Projection(Node):
    def __iter__(self):
        columns = self.args
        self.schema = dict(zip(columns, range(len(columns))))

        for row in self.child:
            yield tuple([row[self.child.schema[column]] for column in self.schema])


class Sort(Node):
    def __iter__(self):
        (col,) = self.args

        rows = list(self.child)
        self.schema = self.child.schema
        rows.sort(key=lambda r: r[self.schema[col]])
        for row in rows:
            yield row
