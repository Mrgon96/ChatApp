import React, { Component } from 'react'
import "./style.css"
import "./login.css"
export class login extends Component {  
    render() {
        return (
            <div className="login">
                <h1>Login</h1>
                <table className="l-table">
                <tr>
                        <td>Username:</td>
                        <td><input type="text" className="input"></input></td>
                </tr>
                <tr>
                        <td>Password:</td>
                        <td><input type="password" className="input"></input></td>
                </tr>
                </table>
                <button className="button" type="submit">Login</button>
            </div>
        )
    }
}

export default login
