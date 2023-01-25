class Tree:
    def __init__(self, symbol=None, parent=None):
        self.symbol = symbol  # char
        self.parent = parent  # Tree
        self.children = {}  # Dictionary {char, Tree}
        self.words = []  # List

    def add_word(self, s):
        current = self
        i = 0
        while i < len(s):
            if s[i] not in current.children.keys():
                current.children[s[i]] = Tree(symbol=s[i], parent=current)
            current = current.children[s[i]]
            i += 1

        while True:
            current.words.append(s)
            if current.parent is not None:
                current = current.parent
            else:
                break

    def search(self, s):
        current = self
        i = 0
        while i < len(s):
            if s[i] not in current.children.keys():
                return False, self
            current = current.children[s[i]]
            i += 1
        if len(current.words) == 0:
            return False, self
        else:
            return True, current

    def delete_word(self, s):
        current = self
        while True:
            current.words.remove(s)
            if current.parent is not None:
                current = current.parent
            else:
                break
