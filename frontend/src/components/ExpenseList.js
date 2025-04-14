import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ExpenseList() {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const response = await axios.get('/api/expenses');
        setExpenses(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load expenses. Please try again later.');
        setLoading(false);
        console.error(err);
      }
    };

    fetchExpenses();
  }, []);

  if (loading) {
    return <div className="card">Loading expenses...</div>;
  }

  if (error) {
    return <div className="card">{error}</div>;
  }

  return (
    <div className="card">
      <h2>Expense History</h2>
      {expenses.length === 0 ? (
        <p>No expenses found. Add your first expense!</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Category</th>
              <th>Item</th>
              <th>Amount ($)</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((expense, index) => (
              <tr key={index}>
                <td>{expense.Date}</td>
                <td>{expense.Category}</td>
                <td>{expense.Item}</td>
                <td>${parseFloat(expense.Amount).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ExpenseList; 