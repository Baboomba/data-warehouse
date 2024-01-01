import { Form, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import './Login.css';
import { useDispatch, useSelector } from "react-redux";
import { loginAsync } from "../../slices/loginSlice";


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
    const [isSaved, setIsSaved] = useState(() => {
        try {
            const saved = localStorage.getItem('isSaved');
            return saved === 'true' ? true : false;
        } catch (error) {
          console.error('Error while retrieving save status:', error);
          return false;
        }
      });

    const handleCheckChange = () => {
        setIsSaved((prev) => {
            const updatedValue = !prev;
            localStorage.setItem('isSaved', updatedValue);
            return updatedValue;
        });
    };

    return (
        <div className="container-memorize">
            <Form>
                <Form.Check
                  checked={isSaved}
                  onChange={handleCheckChange}
                />
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
    const isLogin = useSelector((state) => state.auth.isLoggedIn);
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleLogin = async () => {
        try {
            dispatch(loginAsync({ email, password }));
        } catch(error) {
            console.error('Login failed : ', error);
        }
    };

    useEffect(() => {
        if (isLogin) {
            navigate('/');
        }
    }, [isLogin, navigate]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleLogin()
        }
    };
    
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