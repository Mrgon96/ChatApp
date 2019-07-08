import React, { Component } from 'react'
import "./style.css"
import "./register.css"

export class register extends Component {
    render() {
        return (
            <div className="register">
            <br></br>
                    <h2>Register Here</h2>
                    <table className="r-table">
                    <tr>
                        <td>First Name:</td>
                        <td><input type="text" className="input"></input></td>
                    </tr>
                    <tr>
                        <td>Last Name:</td>
                        <td><input type="text" className="input"></input></td>
                    </tr>
                    <tr>
                        <td>Username:</td>
                        <td><input type="text" className="input"></input></td>
                    </tr>
                    <tr>
                        <td>Password:</td>
                        <td><input type="text" className="input"></input></td>
                    </tr>
                    <tr>
                        <td>Email:</td>
                        <td><input type="text" className="input"></input></td>
                    </tr>
                    <tr>
                        <td colSpan="2"><button className="button" type="submit">Submit</button></td>
                    </tr>
                    </table>             
            </div>
        )
    }
}

export default register
