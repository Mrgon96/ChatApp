import React from 'react';
import PropTypes from 'prop-types';
import './login.css'
import './style.css'

class LoginForm extends React.Component {
  state = {
    username: '',
    password: ''
  };

  handle_change = e => {
    const name = e.target.name;
    const value = e.target.value;
    this.setState(prevstate => {
      const newState = { ...prevstate };
      newState[name] = value;
      return newState;
    });
  };

  render() {
    return (
      <form onSubmit={e => this.props.handle_login(e, this.state)} className="login">
        <h1>Log In</h1>
        <table className="l-table">
        <tr>
            <td>
            <label htmlFor="username">Username</label>
            </td>
            <td>
            <input
                className="input"
                type="text"
                name="username"
                value={this.state.username}
                onChange={this.handle_change}
        />
            </td>
        </tr>
        <tr>
            <td>
            <label htmlFor="password">Password</label>
            </td>
            <td>
            <input
                className="input"
                type="password"
                name="password"
                value={this.state.password}
                onChange={this.handle_change}
        />
        
            </td>
        </tr>
        </table>
        <input className="l-button" type="submit" />
       
       
       
      </form>
    );
  }
}

export default LoginForm;

LoginForm.propTypes = {
  handle_login: PropTypes.func.isRequired
};