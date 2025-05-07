from appengine.components.expenses_components import create_goal_graphs, color, create_graphs
import pandas as pd
import unittest
import os
import json
import datetime

class TestExpensesComponents(unittest.TestCase):
    def setUp(self):
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - datetime.timedelta(days=1)
        self.df = pd.DataFrame({
            'Date': [yesterday, today],
            'Category': ['Food', 'Transport'],
            'Item': ['Pizza', 'Bus Ticket'],
            'Amount': [20.0, 2.5],
            'Username': ['testuser', 'testuser']
        })
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.username = 'testuser'
        self.goals = {
            self.username: {
                'monthly': 500,
                'yearly': 6000
            }
        }
    
    def test_create_graphs(self):
        pie_fig, line_fig = create_graphs(self.df)
        
        # Check if the figures are created
        self.assertIsNotNone(pie_fig)
        self.assertIsNotNone(line_fig)
        
        # Check if the data in the pie chart is correct
        pie_data = pie_fig['data'][0]['values']
        expected_pie_data = [20.0, 2.5]
        self.assertListEqual(list(pie_data), expected_pie_data)
        
        # Check if the data in the line chart is correct
        line_data = line_fig['data'][0]['y']
        expected_line_data = [20.0, 2.5]
        self.assertListEqual(list(line_data), expected_line_data)
    
    def test_create_goal_graphs(self):
        # Set up the goals file for the test user
        goals_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/goals.json'))
        goals_data = {self.username: {'monthly': 500, 'yearly': 6000}}
        os.makedirs(os.path.dirname(goals_path), exist_ok=True)
        with open(goals_path, 'w') as f:
            json.dump(goals_data, f)

        print('DF used in test_create_goal_graphs:', self.df)
        monthly, monthly_label, monthly_color, yearly, yearly_label, yearly_color = create_goal_graphs(self.df, self.username)
        print('monthly:', monthly, 'monthly_label:', monthly_label, 'monthly_color:', monthly_color)
        print('yearly:', yearly, 'yearly_label:', yearly_label, 'yearly_color:', yearly_color)
        
        # Check if the values are correct
        self.assertEqual(monthly, 4.5)
        self.assertEqual(monthly_label, "$500 - 4.5%")
        self.assertEqual(monthly_color, "success")
        
        self.assertEqual(yearly, 0.38)
        self.assertEqual(yearly_label, "$6000 - 0.38%")
        self.assertEqual(yearly_color, "success")

        # Clean up the goals file after test
        os.remove(goals_path)