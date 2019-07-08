import React from 'react';
import PropTypes from 'prop-types';
import './register.css'
class SignupForm extends React.Component {
  state = {
    username: '',
    email:'',
    password: '',
    userdata:
        {
            first_name: '',
            last_name: ''
        }
  };


    handleUserNamechange = (event) =>{
        const username = event.target.value
        this.setState({username:username
        })
    }
    handleEmailchange = (event) =>{
        const email = event.target.value
        this.setState({
            email:email
        })
    }
    handlePasswordchange = (event) =>{
        const password = event.target.value
        this.setState({
            password:password
        })
    }
    handleFisrtchange = (event) =>{
        const First = {...this.state.userdata}
        First.first_name = event.target.value
        this.setState({
            First
        })
    }
    handleLastchange = (event) =>{
        const Last={...this.state.userdata}
        const lname = Last.last_name
        lname = event.target.value
        this.setState({
            last_name:lname
        })
    }

    handleSubmit = (event) => {
        event.preventDefault()

    };
//   handle_change = e => {
//     const name = e.target.name;
//     const value = e.target.value;
//     this.setState(prevstate => {
//       const newState = { ...prevstate };
//       newState[name] = value;
//       return newState;
//     });
//   };



  render() {
    return (
      <form onSubmit={e => this.props.handle_signup(e, this.state)} className="register">
        <h2>Sign Up</h2>
        <table className="r-table">
        <tr>
            <td><label htmlFor="username">Username</label></td>
            <td><input
                    className="input"
                    type="text"
                    name="username"
                    value={this.state.username}
                    onChange={this.handleUserNamechange}
        /></td>
        </tr>
        <tr>
            <td><label htmlFor="userdata.first_name">First Name</label></td>
            <td>
                <input
                    className="input"
                    type="text"
                    name="userdata.first_name"
                    value={this.state.userdata.first_name}
                    onChange={this.handleFisrtchange}
                />
            </td>
        </tr>
        <tr>
            <td><label htmlFor="userdata.last_name">Last Name</label></td>
            <td>
                <input
                    className="input"
                    type="text"
                    name="userdata.last_name"
                    value={this.state.userdata.last_name}
                    onChange={this.handleLastchange}
                />
            </td>
        </tr>
        <tr>
            <td><label htmlFor="email">Email</label></td>
            <td>
                <input
                    className="input"
                    type="email"
                    name="email"
                    value={this.state.email}
                    onChange={this.handleEmailchange}
                />
            </td>
        </tr>
        <tr>
            <td><label htmlFor="password">Password</label></td>
            <td>
                <input
                    className="input"
                    type="password"
                    name="password"
                    value={this.state.password}
                    onChange={this.handlePasswordchange}
                />
            </td>
        </tr>
        </table>

        
       
        <input className="r-button" type="submit" />
      </form>
    );
  }
}

export default SignupForm;

SignupForm.propTypes = {
  handle_signup: PropTypes.func.isRequired
};