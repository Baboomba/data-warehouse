import { useEffect, useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import './Register.css';
import { useNavigate } from "react-router-dom";


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
    const [password2, setPassword2] = useState('');
    const [IsValidated, setIsValidate] = useState(true);
    const [IsRegistered, setIsRegistered] = useState(false);
    const navigate = useNavigate();
    
    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleCheckChange = (e) => {
        setPassword2(e.target.value);
    };

    const checkPassword = () => {
        if (password !== password2) {
            setIsValidate(false);
        } else {
            setIsValidate(true);
        }
        return IsValidated;
    };

    const handleRegister = () => {
        const check = checkPassword();
        console.log(check);
        if (!check) {return ;}

        try {
            const api = 'http://localhost:8000/api/sign-up/'
            const data = {
            email : email,
            password : password,
            password2 : password2
            }
            axios.post(api, JSON.stringify(data) , {
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => {
                if (response.status === 201) {
                    setIsRegistered(true);
                }
            });

        } catch (error) {
            console.log('오류 : ', error.response.status);
            console.log('메시지 : ', error.response.data);
        }
    };

    useEffect(() => {
        if (IsRegistered) {
            window.alert('회원 가입 완료')
            navigate('/login');
        }
    }, [IsRegistered, navigate]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleRegister();
        }
    };

    const responseMsg = () => {
        let msg;
        if (!IsValidated) {
            msg = '* 패스워드가 일치하지 않습니다.';
            return msg;
        }
    }

    return (
        <div className="registerform-bg">
            <TopLabel />
            <InputForm
              onEmailChange={handleEmailChange}
              onPasswordChange={handlePasswordChange}
              onCheckChange={handleCheckChange}
              onKeyDown={handleKeyDown}
            />
            <div className="check-password-label">
                <label>{responseMsg()}</label>
            </div>
            <RegisterBtn onRegister={handleRegister} />
        </div>
    );
};


export { RegisterForm };