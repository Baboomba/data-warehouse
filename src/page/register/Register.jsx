import { useState } from "react";
import { Form, Button } from "react-bootstrap";
import './Register.css';

const TopLabel = () => {
    return (
        <div className="register-label">
            <h3>Sign Up</h3>
        </div>
    );
};

const InputForm = ({ onEmailChange, onPasswordChange, onCheckChange, onKeyDown }) => {
    return (
        <div className="registerinput-bg">
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
                />
                <label htmlFor="floatingPasswordCustom">Password</label>
            </Form.Floating>
            <Form.Floating>
                <Form.Control
                  id="floatingCheckCustom"
                  type="password"
                  placeholder="Password"
                  onChange={onCheckChange}
                  onKeyDown={onKeyDown}
                />
                <label htmlFor="floatingPasswordCustom">Check Password</label>
            </Form.Floating>
        </div>
    );
};

const RegisterBtn = ({ onRegister }) => {
    return (
        <div className="register-btn-bg">
            <Button
              className="register-btn"
              size="lg"
              onClick={onRegister}
            >
                <label>회원 가입</label>
            </Button>
        </div>
    );
};


const RegisterForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [check, setCheck] = useState('');
    const [IsValidated, setIsValidate] = useState(true);

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleCheckChange = (e) => {
        setCheck(e.target.value);
    };

    const handleRegister = () => {
        if (password !== check) {
            setIsValidate(false);
        } else {
            setIsValidate(true);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleRegister();
        }
    };

    return (
        <div className="registerform-bg">
            <TopLabel />
            <InputForm
              onEmailChange={handleEmailChange}
              onPasswordChange={handlePasswordChange}
              onCheckChange={handleCheckChange}
              onKeyDown={handleKeyDown}
              onRegister={handleRegister}
            />
            <label
              className={
                IsValidated ?
                'true-password-label' :
                'false-password-label'
              }
            >
                * 패스워드가 일치하지 않습니다.
            </label>
            <RegisterBtn onRegister={handleRegister} />            
        </div>
    );
};


export { RegisterForm };