import { Form, Button } from "react-bootstrap";
import { useState } from "react";
import './Login.css';

const TopLabel = () => {
    return (
        <div>
            <h3>SIGN IN</h3>
        </div>
    );
}

const InputForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
        console.log(e.target.value);
    };
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        console.log(e.target.value);
    }

    return (
        <div className="inputform-bg">
            <Form.Floating className="mb-3">
                <Form.Control
                  id="floatingInputCustom"
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={handleEmailChange}
                />
                <label htmlFor="floatingInputCustom">Email address</label>
            </Form.Floating>
            <Form.Floating>
                <Form.Control
                  id="floatingPasswordCustom"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={handlePasswordChange}
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

const SubmitBtn = () => {
    return (
        <div className="loginbtn-bg">
            <Button
              variant='primary'
              size="lg"
              className="login-btn"
            >
                <label>로그인</label>
            </Button>
        </div>
    );
};

const LoginForm = () => {
    return (
        <div className="loginform-bg">
            <TopLabel />
            <InputForm />
            <MemorizeInfo />
            <SubmitBtn />
        </div>
    );
};

export { LoginForm };