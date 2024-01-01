import { Container, Row, Col } from "react-bootstrap";
import './Home.css';
import { LoginForm } from "../login/Login";
import SideMenu from "../../component/sideMenu/SideMenu";
import { RegisterForm } from "../register/Register";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { CenterHeader, RightHeader } from "../../component/header/Header";
import { MainContent } from "../../component/content/main/Main";
import { useSelector } from "react-redux";


const Main = () => {
    const navigate = useNavigate();
    const isLoggedIn = useSelector((state) => state.auth.isLoggedIn);

    useEffect(() => {
        const checkLogin = () => {
            if (isLoggedIn !== true) {
                navigate('/login');
            }
        };

        checkLogin();
    }, [isLoggedIn, navigate]);
    
    return (
        <div>
            <div className="main-body">
                <div className="main-grid-left">
                    <SideMenu />
                </div>
                <div className="main-grid-center">
                    <div className="main-center-header">
                        <CenterHeader />
                    </div>
                    <div className="main-center-content">
                        <MainContent />
                    </div>
                </div>
                <div className="main-grid-right">
                    <div className="main-right-header">
                        <RightHeader />
                    </div>
                    <div className="main-right-content">
                        right content
                    </div>
                </div>
            </div>
            <div className="main-grid-footer">footer</div>
        </div>
    );
};

const Login = () => {
    return (
        <div>
            <Container fluid>
                <Row className="login-grid-full">
                    <Col xxl={3} className="login-grid-center">
                        <LoginForm></LoginForm>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

const Register = () => {
    return (
        <div>
            <Container>
                <Row className="register-grid-full">
                    <Col xxl={3} className="register-grid-center">
                        <RegisterForm></RegisterForm>
                    </Col>
                </Row>
            </Container>
        </div>
    )
}

export { Main, Login, Register };