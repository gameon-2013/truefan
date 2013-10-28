from django.test import TestCase
from django.db.utils import IntegrityError
from models import *

class KeywordModelTest(TestCase):

    def test_create_keyword(self):
        k = Keyword()
        self.assertNotEqual(k, None, "Can't create keyword")

    def test_store_keyword(self):
        k = Keyword(value='rugby')
        k.save()

        keywords = Keyword.objects.all();

        self.assertEqual(len(keywords), 1, "Keyword not saved")
        self.assertIn(k, keywords, "Keyword not in list of saved keywords")
    
    def test_keyword_uniqueness(self):
        ''' fails if an error is not raised when saving 2 similar keywords '''
        k = Keyword(value='ruj')
        k.save()

        k2 = Keyword(value='ruj')

        self.assertRaises(IntegrityError, k2.save)

class RegexTest(TestCase):
    ''' test regex construct in keywords '''
    
    def setUp(self):
        self.keywords = ['rugby', 'ruj', 'sevens']
        for i in self.keywords:
            Keyword.objects.create(value=i)

    def test_regex(self):
        test_rx = "|".join(self.keywords)
        self.assertEqual(test_rx, Keyword.regex(), "Regex did not match")

    def test_match(self):
        sample = "This is rugby sevens"
        results = Keyword.match(sample)

        self.assertEqual(len(results), 2, "Wrong number of matches")
        self.assertIn('rugby', results, "Rugby not one of the results of the match")