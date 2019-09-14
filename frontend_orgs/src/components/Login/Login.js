import React, { Component } from 'react';
import {Form, Icon, Input, Button, notification } from 'antd';
import 'antd/es/date-picker/style/css';
import './Login.css'
import api, {setSid, setUsername, setAccess} from "../../api/api";
import {BrowserView} from "react-device-detect";
import logo from '../../assets/logo_ph.png'



class LoginForm extends Component {

    state = {
        loading: false,
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.setState({loading: true});
                api.post("/auth/login/", {"email": values.userName, "password": values.password}).then( resp => {
                    setUsername(values.userName);
                    setSid(resp.data.IDtoken);
                    setAccess(resp.data.accesToken);
                    this.setState({loading: false});
                    this.props.history.push("/home");
                }).catch((error) => {
                    if (error.response) {
                        notification['error']({
                            message: 'Invalid parameters',
                            description: "Incorrect username or password",
                        });
                        this.setState({loading: false});
                    }
                });
            }
        });
    };

    render() {
        const { getFieldDecorator } = this.props.form;
        const {loading} = this.state;

        return (
            <BrowserView>
                <Form onSubmit={this.handleSubmit} className="login-form">
                    <div className="login-background"/>
                    <img src={logo} alt="Logo" className="image-logo"/>
                    <Form.Item>
                        {getFieldDecorator('userName', {
                            rules: [{required: true, message: 'Please input your username!'}]
                        })(
                            <Input className="login-input" prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>} placeholder="Username"/>
                        )}
                    </Form.Item>

                    <Form.Item>
                        {getFieldDecorator('password', {
                            rules: [{required: true, message: 'Please input your Password!'}],
                        })(
                            <Input.Password className="login-input" prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>} placeholder="Password"/>
                        )}
                    </Form.Item>
                    {loading ?
                        <img src='https://i1.wp.com/www.sportsmonks.com/wp-content/uploads/2018/loading.gif' alt='' style={{width: '10%', marginLeft: '47%', marginTop: '5%', marginBottom: '5%'}}/> :
                        <Form.Item className="formItem-form">
                            <Button type="primary" htmlType="submit" className="login-form-button"> Log in </Button>
                            Don't you have an account yet? <a href="/register" className="hyper-form">Register Now!</a>
                        </Form.Item>
                    }
                </Form>
            </BrowserView>
        );
    };
}

const Login = Form.create({ name: 'login' })(LoginForm);
export default Login;