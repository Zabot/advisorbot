import json
import re
import random

# Load the JSON descriptions of the classes
with open('data/classes.json') as course_info:
    classes = json.load(course_info)

# Store each classes key in the class info object
for prefix, clazz in classes.items():
    for number in clazz:
        classes[prefix][number]["short"] = prefix + " " + number

# Load the JSON storing bot responses
with open('data/responses.json') as keywords_json:
    keywords = json.load(keywords_json)

# Matches any valid course prefix followed by a three digit number
# First capture group is the prefix, second is the course number
course = "("+ "|".join( classes.keys() ) +")?\s*(\d{3}|BS)"

# A dict of keyword regexs to appropriate responses
keywords = {"|".join(key["keywords"]):key["response"] for key in keywords}

# Returns a response appropriate for the the string s
def handle(s):
    try:
        # Grab all of the classes mentioned in s (If no prefix, assume CS)
        names_mentioned = [ (match[0] if match[0] else "CS", match[1]) for match in re.findall(course, s.upper()) ]
        classes_mentioned = [ classes[ name[0] ][  name[1] ] for name in names_mentioned if name[1] in classes[name[0]]]

        if len(names_mentioned) != len(classes_mentioned):
            return "That class does not exist"

        # Grabs all of the responses that would be appropriate for the located keywords
        responses = [response for regex, response in keywords.items() if re.search(regex, s.lower()) is not None ]

        # If we didn't find any keywords in the string, give up
        if not responses:
            return "I'm sorry, I don't understand you. Please try something else."

        # Assume 1 keyword and 1 class mentioned
        response = responses[ 0 ][ random.randint( 0, len(responses[0]) - 1 ) ]

        # Substitute the requested info into the response
        return re.sub("\$(\w+)(?:\((\w+)\))?", lambda m: substitute(m.group(1), m.group(2), classes_mentioned), response)

    except Exception as e:
        return "An exception occured: <" + s + "> `" + str(e) +"`"

# Replaces a $identifier in a response with whatever is returned by this function
def substitute(identifier, arg, mentioned):
    interested = get_class_by_name(arg) if arg else mentioned[0]

    # Check for keywords that aren't directly from json
    if identifier == "prereq_tree":
        return build_prereq_tree(interested, 0, {0:True})

    elif identifier == "prereqs":
        if not "prereqs" in interested:
            return "no prerequisites"

    # Fetch requested info from JSON
    info = interested[identifier]

    # Expand lists to make gramatical sense
    if isinstance(info, list):
        return expand_list(info)
    
    return info

# Builds up a tree view of course prerequisites where each parent-child relationship represents a prequisite
def build_prereq_tree(c, depth, ended):
    tree = ""
    for i in range(0, depth - 1):
        tree += "  " if ended[i] else "│ "

    tree += ("" if depth == 0 else ("└─" if ended[depth] else "├─")) + c["short"] + "\n"

    # If there are no prereqs to this class, we are done
    if not "prereqs" in c:
        return tree

    ended[depth] = False
    for p in [ get_class_by_name(prereq) for prereq in c["prereqs"][0:-1] ]:
        ended[depth + 1] = False
        tree += build_prereq_tree(p, depth + 1, ended)

    ended[depth] = True
    ended[depth + 1] = True
    tree += build_prereq_tree(get_class_by_name(c["prereqs"][-1]), depth + 1, ended)

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

# Gets the json info associated with a particular class name
def get_class_by_name(name):
    match = re.match("([A-Z]+) ?(\d{3})", name)
    return classes[ match[1] ][ match[2] ]

