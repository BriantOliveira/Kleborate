"""
Copyright 2018 Kat Holt
Copyright 2018 Ryan Wick (rrwick@gmail.com)
https://github.com/katholt/Kleborate/

This file is part of Kleborate. Kleborate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kleborate is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kleborate. If
not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from kleborate.kleborate import get_data_path, get_output_headers, get_resistance_results


class Args(object):
    def __init__(self):
        self.resistance = True
        self.kaptive_k = False
        self.kaptive_o = False


class TestResMgrBPmrB(unittest.TestCase):
    """
    Tests calling of colistin resistance via the truncation of mgrB/pmrB.
    """

    def setUp(self):
        self.args = Args()
        self.data_dir = get_data_path()
        _, _, self.res_headers = get_output_headers(self.args, self.data_dir)

    def test_both_genes_intact(self):
        results = get_resistance_results(self.data_dir, 'test/sequences/test_res_mgrb_pmrb_1.fasta',
                                         self.args, self.res_headers, True)
        self.assertEqual(results['Col'], '-')

    def test_pmrb_frameshift(self):
        """
        A frameshift in pmrB should cause an early stop and lead to a colisitin resistance call.
        """
        results = get_resistance_results(self.data_dir, 'test/sequences/test_res_mgrb_pmrb_2.fasta',
                                         self.args, self.res_headers, True)
        self.assertTrue('PmrB-' in results['Col'])

    def test_pmrb_early_stop(self):
        """
        This tests an early stop mutation (without a frameshift) in pmrB.
        """
        results = get_resistance_results(self.data_dir, 'test/sequences/test_res_mgrb_pmrb_3.fasta',
                                         self.args, self.res_headers, True)
        self.assertTrue('PmrB-' in results['Col'])

    def test_mgrb_missing(self):
        results = get_resistance_results(self.data_dir, 'test/sequences/test_res_mgrb_pmrb_4.fasta',
                                         self.args, self.res_headers, True)
        self.assertTrue('MgrB-' in results['Col'])

    def test_mgrb_missing_non_kp_complex(self):
        """
        Setting the Kp complex variable to False should turn off the MgrB/PmrB tests.
        """
        results = get_resistance_results(self.data_dir, 'test/sequences/test_res_mgrb_pmrb_4.fasta',
                                         self.args, self.res_headers, False)
        self.assertTrue('MgrB-' not in results['Col'])

    def test_pmrb_early_stop_SRR2098701(self):
        results = get_resistance_results(self.data_dir, 'test/sequences/SRR2098701.fasta',
                                         self.args, self.res_headers, True)
        self.assertTrue('PmrB-' in results['Col'])
