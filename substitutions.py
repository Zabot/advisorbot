def title(clazz):
    return clazz["title"]

def number(clazz):
    return clazz["number"]

def desc(cazz):
    return clazz["desc"]

def prereqs(clazz):
    return expand_list([p["number"] for p in clazz["prereqs"] ])

def teachers(clazz):
    return expand_list([p["teachers"] for p in clazz["teachers"] ])

# Builds up a tree view of course prerequisites where each parent-child relationship represents a prequisite
def prereq_tree(root, depth=0, ended={0:True}):
    tree = ""
    for i in range(0, depth - 1):
        tree += "  " if ended[i] else "│ "

    tree += ("" if depth == 0 else ("└─" if ended[depth] else "├─")) + root["number"] + "\n"

    # If there are no prereqs to this class, we are done
    if not "prereqs" in root:
        return tree

    ended[depth] = False
    for p in root["prereqs"][0:-1]:
        ended[depth + 1] = False
        tree += prereq_tree(p, depth + 1, ended)

    ended[depth] = True
    ended[depth + 1] = True
    tree += prereq_tree(root["prereqs"][-1], depth + 1, ended)

    return tree


# Expands a list with commas and a conjunction
# [1] -> 1
# [1, 2] -> 1 and 2
# [1, 2, ..., n] -> 1, 2, ... , and n
def expand_list(lst, conjunction="and"):
    string = ", ".join(lst[0:-1])

    if len(lst) > 2:
        return string + ", " + conjunction + " " + lst[-1]
    elif len(lst) > 1:
        return string + " " + conjunction + " " + lst[-1]
    else:
        return lst[-1]
