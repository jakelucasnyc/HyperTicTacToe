import React from 'react';
import Game from './game/Game'
import Home from './home/Home'
import GameDB from './gameDB/GameDB'
import { Route, Link } from 'react-router-dom'
import Navbar from './Navbar'
// import 'rsuite/dist/styles/rsuite-default.css';

export default function App() {


  return (
    <div className="App">
    	<Navbar/>
	    	<Route exact path="/" component={Home}/>
	    	<Route exact path="/database" component={GameDB}/>
	    	<Route exact path="/game" component={Game}/>

    </div>
  );
}
