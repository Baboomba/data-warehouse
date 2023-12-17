import { Container, Row, Col } from "react-bootstrap";
import './Home.css';
import { LoginForm } from "../login/Login";
import SideMenu from "../../component/sideMenu/SideMenu";
import { RegisterForm } from "../register/Register";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { CenterHeader, RightHeader } from "../../component/header/Header";


const Main = () => {
    const navigate = useNavigate();
    const checkLogin = () => {
        const value = sessionStorage.getItem('isLoggedIn');
        if (!value) {
            navigate('/login');
        }
    };

    useEffect(() => {
        checkLogin();
    })
    
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
                    <div className="main-center-content">Content
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
            
            {/* <Container fluid>
                <Row>
                    <Col md={2} className="main-grid-left">
                        <SideMenu />
                    </Col>
                    <Col md={8} className="main-grid-center">
                        <Row className="main-center-header">
                            <Header />
                        </Row>
                        <Row className="main-center-content">Content
                        </Row>
                    </Col>
                    <Col md={2} className="main-grid-right">
                        <Row className="main-right-header">right</Row>
                        <Row className="main-right-content">right content</Row>
                    </Col>
                </Row>
                <Row className="main-grid-footer">footer</Row>
            </Container> */}
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