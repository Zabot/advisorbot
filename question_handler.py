import json
import re
import random
import substitutions

# Load the JSON descriptions of the classes
with open('data/classes.json') as course_info:
    classes = json.load(course_info)

# Gets the json info associated with a particular class name
def get_class_by_name(name):
    match = re.match("([A-Z]+) ?(\d{3})", name)
    return classes[ match[1] ][ match[2] ]

# Store each classes number in the class info object and inflate the prerequiste graph
for prefix, numbers in classes.items():
    for number, clazz in numbers.items():
        clazz["number"] = prefix + " " + number

        if "prereqs" in clazz:
            clazz["prereqs"] = [ get_class_by_name(prereq) for prereq in clazz["prereqs"] ]

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
        names_mentioned = [ " ".join((match[0] if match[0] else "CS", match[1])) for match in re.findall(course, s.upper()) ]

        # Grabs all of the responses that would be appropriate for the located keywords
        responses = [response for regex, response in keywords.items() if re.search(regex, s.lower()) is not None ]

        # If we didn't find any keywords in the string, give up
        if not responses:
            return "I'm sorry, I don't understand you. Please try something else."

        # Assume 1 keyword and 1 class mentioned
        response = responses[ 0 ][ random.randint( 0, len(responses[0]) - 1 ) ]

        # Substitute the requested info into the response
        return re.sub("\$(\w+)\(([\w\[\]]*)\)", lambda m: substitute(m.group(1), names_mentioned, [arg.strip() for arg in m.group(2).split(",")]), response)

    except Exception as e:
        return "An exception occured: <" + s + "> `" + str(e) +"`"

def substitute(identifier, mentioned, args):
    # If any of the arguments request mentioned classes, substitute now
    args = [ re.sub("m\[(\d)\]", lambda m: mentioned[int(m[1])], arg) for arg in args ]

    # Now substitute class numbers for class objects
    args = [ get_class_by_name(arg) for arg in args if re.match("([A-Z]+) ?(\d{3})", arg) ]

    # Call the subsitution function
    substitution = getattr(substitutions, identifier)
    if substitution:
        return substitution(*args)
    return "BAD SUBSTITUTION"

