import pytest
import os
import sys

sys.path.append(os.path.abspath('../src'))

from cost_optimizer import CostOptimizer

def test_valid1():
    co = CostOptimizer(config_path='../config')
    EXPECTED = {
        'Output': [
            {
                'region': 'New York',
                'total_cost': '$10150',
                'machines': [
                    ('8XLarge', 7),
                    ('XLarge', 1),
                    ('Large', 1)
                ]
            },
            {
                'region': 'India',
                'total_cost': '$9520',
                'machines': [
                    ('8XLarge', 7),
                    ('Large', 3)
                ]
            },
            {
                'region': 'China',
                'total_cost': '$8570',
                'machines': [
                    ('8XLarge', 7),
                    ('XLarge', 1),
                    ('Large', 1)
                ]
            }
        ]
    }
    assert EXPECTED == co.optimize(1150, 1)

def test_valid2():
    co = CostOptimizer(config_path='../config')
    EXPECTED = {
        'Output': [
            {
                'region': 'New York',
                'total_cost': '$11000',
                'machines': [
                    ('8XLarge', 1),
                    ('2XLarge', 1),
                    ('XLarge', 1),
                    ('Large', 1)
                ]
            },
            {
                'region': 'India',
                'total_cost': '$10665',
                'machines': [
                    ('8XLarge', 1),
                    ('2XLarge', 1),
                    ('Large', 3)
                ]
            },
            {
                'region': 'China',
                'total_cost': '$9450',
                'machines': [
                    ('8XLarge', 1),
                    ('XLarge', 3),
                    ('Large', 1)
                ]
            }
        ]
    }
    assert EXPECTED == co.optimize(230, 5)

def test_valid3():
    co = CostOptimizer(config_path='../config')
    EXPECTED = {
        'Output': [
            {
                'region': 'New York',
                'total_cost': '$24096',
                'machines': [
                    ('4XLarge', 1),
                    ('XLarge', 1)
                ]
            },
            {
                'region': 'India',
                'total_cost': '$26544',
                'machines': [
                    ('2XLarge', 2),
                    ('Large', 2)
                ]
            },
            {
                'region': 'China',
                'total_cost': '$20880',
                'machines': [
                    ('4XLarge', 1),
                    ('XLarge', 1)
                ]
            }
        ]
    }
    assert EXPECTED == co.optimize(100, 24)

def test_valid4():
    co = CostOptimizer(config_path='../config')
    EXPECTED = {
        'Output': [
            {
                'region': 'New York',
                'total_cost': '$118248',
                'machines': [
                    ('8XLarge', 6),
                    ('4XLarge', 1),
                    ('2XLarge', 1),
                    ('XLarge', 1)
                ]
            },
            {
                'region': 'India',
                'total_cost': '$111828',
                'machines': [
                    ('8XLarge', 6),
                    ('2XLarge', 3),
                    ('Large', 2)
                ]
            },
            {
                'region': 'China',
                'total_cost': '$100200',
                'machines': [
                    ('8XLarge', 6),
                    ('4XLarge', 1),
                    ('XLarge', 3)
                ]
            }
        ]
    }
    assert EXPECTED == co.optimize(1100, 12)

def test_invalid1():
    co = CostOptimizer(config_path='../config')
    assert not co.optimize(203, 2)

def test_invalid2():
    try:
        CostOptimizer(config_path='junk_path')
    except FileNotFoundError:
        assert True
    except:
        assert False