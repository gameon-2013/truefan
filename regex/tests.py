from django.test import TestCase
from django.db.utils import IntegrityError
from django_webtest import WebTest
from models import *

class KeywordModelTest(TestCase):

    def test_create_keyword(self):
        k = Keyword()
        self.assertNotEqual(k, None, "Can't create keyword")

    def test_store_keyword(self):
        k = Keyword(value='rugby')
        k.save()

        keywords = Keyword.objects.all()

        self.assertEqual(len(keywords), 1, "Keyword not saved")
        self.assertIn(k, keywords, "Keyword not in list of saved keywords")
    
    def test_keyword_uniqueness(self):
        ''' fails if an error is not raised when saving 2 similar keywords '''
        k = Keyword(value='ruj')
        k.save()

        k2 = Keyword(value='ruj')

        self.assertRaises(IntegrityError, k2.save)

        # BUG: uniqueness should be case insensitive
        # k2 = Keyword(value='Ruj')
        # self.assertRaises(IntegrityError, k2.save)

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

class KeywordViewsTest(WebTest):
    ''' test views dealing with keywords '''
    csrf_checks = False

    def test_add_keyword(self):
        ''' test addition of single keyword '''
        keyword = 'rugby'

        keywords_page = self.app.get('/regex/keywords').follow()

        form = keywords_page.form

        form['value'] = keyword
        form.submit().follow()

        keywords = Keyword.objects.all()
        self.assertEqual(len(keywords), 1, "Keyword was not saved: "+repr(keywords))
        self.assertEqual(keyword, keywords[0].value, "Keyword was not saved: "+repr(keywords[0]))

    def test_unique_keyword(self):
        ''' should fail when the same keyword is entered '''
        keyword = 'rugby'

        Keyword.objects.create(value=keyword)
        keywords = Keyword.objects.all()
        self.assertEqual(len(keywords), 1, "Test keyword not added: %s" % repr(keywords))

        keywords_page = self.app.get('/regex/keywords').follow()

        form = keywords_page.form
        form['value'] = keyword
        response = form.submit()

        self.assertEqual(200, response.status_code, "Wrong status code: %s" % repr(response.status_code))
        self.assertIn('already exists', response, "Error message not shown: %s" % response.content)

        keywords = Keyword.objects.all()
        self.assertEqual(len(keywords), 1, "Unique keyword was saved: "+repr(keywords))

    def test_bulk_entry(self):
        ''' test adding more than one keyword at a time '''
        keywords = ['rugby', 'ruj', 'sevens']
        keywords_string = ",".join(keywords)

        bulk_page = self.app.get('/regex/bulk_keywords').follow()

        form = bulk_page.form
        form['value'] = keywords_string
        response = form.submit().follow()

        self.assertEqual(200, response.status_code, "Wrong status code: %s" % repr(response.status_code))        

        keywords = Keyword.objects.all()
        self.assertEqual(len(keywords), 3, "Keywords were not stored: %s" % repr(keywords))
        self.assertIn('rugby', [i.value for i in keywords], "Rugby not in keywords stored: %s" % repr(keywords))

class MatchViewTest(WebTest):
    ''' tests views dealing with matching samples '''

    def setUp(self):
        self.keywords = ['rugby', 'ruj', 'sevens']
        for i in self.keywords:
            Keyword.objects.create(value=i)

    def test_positive_match(self):
        ''' test matching a sample '''
        sample = "This is rugby sevens"
        match_page = self.app.get('/regex/match').follow()

        form = match_page.form
        form['sample'] = sample
        response = form.submit()

        self.assertEqual(200, response.status_code, "Wrong status code: %s" % repr(response.status_code))
        self.assertIn('rugby', response, "Rugby not in response: %s" % response.content)
        self.assertIn('sevens', response, "Sevens not in response: %s" % response.content)
