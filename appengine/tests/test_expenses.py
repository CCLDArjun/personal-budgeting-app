from components.expenses_components import create_goal_graphs, color, create_graphs
import pandas as pd
import unittest

class TestExpensesComponents(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02'],
            'Category': ['Food', 'Transport'],
            'Item': ['Pizza', 'Bus Ticket'],
            'Amount': [20.0, 2.5],
            'Username': ['testuser', 'testuser']
        })
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
        self.assertEqual(pie_data, expected_pie_data)
        
        # Check if the data in the line chart is correct
        line_data = line_fig['data'][0]['y']
        expected_line_data = [20.0, 2.5]
        self.assertEqual(line_data, expected_line_data)
    
    def test_create_goal_graphs(self):
        monthly, monthly_label, monthly_color, yearly, yearly_label, yearly_color = create_goal_graphs(self.goals, self.username)
        
        # Check if the values are correct
        self.assertEqual(monthly, 4.0)
        self.assertEqual(monthly_label, "$500 - 4.0%")
        self.assertEqual(monthly_color, 0)
        
        self.assertEqual(yearly, 0.08333333333333333)
        self.assertEqual(yearly_label, "$6000 - 0.08333333333333333%")
        self.assertEqual(yearly_color, 0)