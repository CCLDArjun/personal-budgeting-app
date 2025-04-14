import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function AddExpense() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    category: '',
    item: '',
    amount: ''
  });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      await axios.post('/api/expenses', formData);
      setSubmitting(false);
      navigate('/expenses'); // Redirect to expenses page after successful submission
    } catch (err) {
      setError('Failed to add expense. Please try again.');
      setSubmitting(false);
      console.error(err);
    }
  };

  return (
    <div className="card">
      <h2>Add New Expense</h2>
      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="date">Date:</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>
        
        <div>
          <label htmlFor="category">Category:</label>
          <input
            type="text"
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            placeholder="e.g., Groceries, Entertainment, Utilities"
            required
          />
        </div>
        
        <div>
          <label htmlFor="item">Item:</label>
          <input
            type="text"
            id="item"
            name="item"
            value={formData.item}
            onChange={handleChange}
            placeholder="Description of expense"
            required
          />
        </div>
        
        <div>
          <label htmlFor="amount">Amount ($):</label>
          <input
            type="number"
            id="amount"
            name="amount"
            step="0.01"
            min="0.01"
            value={formData.amount}
            onChange={handleChange}
            placeholder="0.00"
            required
          />
        </div>
        
        <button type="submit" disabled={submitting}>
          {submitting ? 'Adding...' : 'Add Expense'}
        </button>
      </form>
    </div>
  );
}

export default AddExpense; 