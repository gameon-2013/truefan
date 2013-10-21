__author__ = 'caninemwenja'

import utils
import sys

def test_raw_keywords():
    if len(sys.argv) < 3:
        print 'Usage: %s keywords_file target_file [target_file] ....' % sys.argv[0]
        return
    
    keyword_file = sys.argv[1]
    target_files = sys.argv[2:]

    for i in target_files:
        log_file = "target_log_%s-%s.csv" % (keyword_file, i)
        utils.test_match(keyword_file, i, log_file)

if __name__ == "__main__":
    test_raw_keywords()
