import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home';
import ExpenseList from './components/ExpenseList';
import AddExpense from './components/AddExpense';

function App() {
  return (
    <div className="container">
      <header className="card">
        <h1>Money Maestro</h1>
        <nav>
          <Link to="/" className="button">Home</Link>
          <Link to="/expenses" className="button" style={{ marginLeft: '10px' }}>Expenses</Link>
          <Link to="/add" className="button" style={{ marginLeft: '10px' }}>Add Expense</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/expenses" element={<ExpenseList />} />
        <Route path="/add" element={<AddExpense />} />
      </Routes>
    </div>
  );
}

export default App; 