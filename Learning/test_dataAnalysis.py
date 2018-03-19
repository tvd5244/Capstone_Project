#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 04:42:58 2018

@author: Taras_Derewecki
"""

import unittest
import dataAnalysis

class TestDataAnalysis(unittest.TestCase):
    
    def test_tokenize(self):
        result1 = dataAnalysis.tokenize('hello world')
        self.assertEqual(result1, 'hello', 'world')
        
        result2 = dataAnalysis.tokenize('')
        self.assertEqual(result2, '[]')
        
        result3 = dataAnalysis.tokenize('hello')
        self.assertEqual(result3, 'hello')
        
        result4 = dataAnalysis.tokenize(' ')
        self.assertEqual(result4, '[]')
    