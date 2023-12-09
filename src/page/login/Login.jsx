import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import { Link } from "react-router-dom";
import './Login.css';

const TopLabel = () => {
    return (
        <div>
            <h3>SIGN IN</h3>
        </div>
    );
}

const InputForm = ({ onEmailChange, onPasswordChange, onKeyDown }) => {
    return (
        <div className="inputform-bg">
            <Form.Floating className="mb-3">
                <Form.Control
                  id="floatingInputCustom"
                  type="email"
                  placeholder="name@example.com"
                  onChange={onEmailChange}
                />
                <label htmlFor="floatingInputCustom">Email address</label>
            </Form.Floating>
            <Form.Floating>
                <Form.Control
                  id="floatingPasswordCustom"
                  type="password"
                  placeholder="Password"
                  onChange={onPasswordChange}
                  onKeyDown={onKeyDown}
                />
                <label htmlFor="floatingPasswordCustom">Password</label>
            </Form.Floating>
        </div>
    );
};

const MemorizeInfo = () => {
    return (
        <div className="container-memorize">
            <Form>
            <Form.Check />
            </Form>
            <label className="label-memorize">
                아이디 기억하기
            </label>
        </div>
    );
};

const SubmitBtn = ({ onLogin }) => {
    return (
        <div className="loginbtn-bg">
            <Button
              variant='primary'
              size="lg"
              className="login-btn"
              onClick={onLogin}
            >
                <label>로그인</label>
            </Button>
        </div>
    );
};

const RegisterLink = () => {
    return (
        <div className="register-link">
            <Link to='/register'>
                <label>회원가입</label>
            </Link>
        </div>
    );
};

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }

    const handleLogin = async () => {
        fetch('http://localhost:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
            })
        })
        .then(response => {
            if(!response.ok) {
                throw new Error('Login failed');
            }
            console.log('Login successful');
            return response.json();
        })
        .catch(error => {
            console.error('error during login', error);
        });
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleLogin()
        }
    }
    
    return (
        <div className="loginform-bg">
            <TopLabel />
            <InputForm
              onEmailChange={handleEmailChange}
              onPasswordChange={handlePasswordChange}
              onKeyDown={handleKeyDown}
            />
            <MemorizeInfo />
            <SubmitBtn onLogin={handleLogin} />
            <RegisterLink />
        </div>
    );
};

export { LoginForm };