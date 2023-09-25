import textwrap
import unittest

import pandoc_purl

from purl_test import PurlTest

class TestInline(PurlTest):
    def test_expression(self):
        source = "Hello `1+1`{.p} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'},
                {'t': 'Str', 'c': '2'},
                {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        altered = self._purl(source)
        self.assertEqual(baseline, altered["blocks"])
    
    def test_no_eval(self):
        source = "Hello `1+1`{.p eval=false} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'},
                {'t': 'Code', 'c': [['', ['p'], []], '1+1']},
                {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        altered = self._purl(source)
        self.assertEqual(baseline, altered["blocks"])
    
    def test_asis(self):
        source = "Hello `1+1`{.p results=asis} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'},
                {'t': 'Str', 'c': '2'},
                {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        altered = self._purl(source)
        self.assertEqual(baseline, altered["blocks"])
    
    def test_hide(self):
        source = "Hello `1+1`{.p results=hide} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'}, {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        altered = self._purl(source)
        self.assertEqual(baseline, altered["blocks"])
    
    def test_markup_inline(self):
        source = "Hello `f'**{1+1}**'`{.p results=markup} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'},
                {'t': 'Strong', 'c': [{'t': 'Str', 'c': '2'}]},
                {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        altered = self._purl(source)
        self.assertEqual(baseline, altered["blocks"])
    
    def test_markup_block(self):
        source = "Hello `'# header'`{.p results=markup} world"
        baseline = [
            {'t': 'Para', 'c': [
                {'t': 'Str', 'c': 'Hello'},
                {'t': 'Space'},
                {'t': 'Strong', 'c': [{'t': 'Str', 'c': '2'}]},
                {'t': 'Space'},
                {'t': 'Str', 'c': 'world'}]}]
        
        with self.assertRaises(Exception):
            self._purl(source)
    
if __name__ == "__main__":
    unittest.main()
