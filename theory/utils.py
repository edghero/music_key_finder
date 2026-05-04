def format_sequence(items):
    return " - ".join(items)


def normalize_root(root):
    root = root.strip()
    if not root:
        return root
    return root[0].upper() + root[1:].lower()
