import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="card">
      <h2>Welcome to Money Maestro</h2>
      <p>Your personal budgeting application to help you track and manage your expenses.</p>
      <div>
        <Link to="/expenses" className="button">View Expenses</Link>
        <Link to="/add" className="button" style={{ marginLeft: '10px' }}>Add New Expense</Link>
      </div>
    </div>
  );
}

export default Home; 