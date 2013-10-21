__author__ = 'caninemwenja'

import re

def match_file(filename, matcher):
    f = open(filename)
    data = f.read()
    f.close()

    results = []
    
    lines = [i.strip() for i in data.split("\n")]
    count = 0
    for i in lines:
        matches = matcher.findall(i)
        if len(matches) > 0:
            results.append((count, i, matches))
        count = count + 1
    
    return (results, len(lines))

def matcher(keyword_file):
    f = open(keyword_file)
    data = f.read()
    f.close()
    
    keywords = [i.strip() for i in data.split(",")]
    regex = "|".join(keywords)
    return re.compile(regex, re.IGNORECASE)

def test_match(keyword_file, target_file, log_file=None):
    compiler = matcher(keyword_file)
    results = match_file(target_file, compiler)

    if log_file:
        f = open(log_file, "w")
        for i in results[0]:
            f.write("line %i" % i[0])
            f.write(", ")
            f.write(i[1])
            f.write(", ")
            f.write(repr(i[2]))
            f.write(", ")
            f.write(repr(len(i[2])))
            f.write("\n")
        f.close()

    print "%i matched out of %i lines of %s" % (len(results[0]), results[1], target_file)
    return results
