import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
	return (
		<nav className="navbar navbar-light" style={{ backgroundColor: "#FF7F50" }}>
		  
		  <div className="container-md">
		    <a className="navbar-brand" href="/">Home</a>
		    <a className="navbar-brand" href="/database">Game Database</a>

		    <form className="d-flex">
		      <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search"></input>
		      <button className="btn btn-outline-success" type="submit">Search</button>
		    </form>
		  </div>
		   
		</nav>
	)
}