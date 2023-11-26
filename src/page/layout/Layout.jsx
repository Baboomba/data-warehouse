import { Container, Row, Col } from "react-bootstrap";
import './Layout.css';
import { LoginForm } from "../login/Login";

const Main = () => {
    return (
        <div>
            <Container fluid>
                <Row>
                    <Col xxl={2} className="main-grid-left">
                    </Col>
                    <Col className="main-grid-right">
                        <Row className="main-grid-header">
                        </Row>
                        <Row className="main-grid-content">
                        </Row>
                    </Col>
                </Row>
                <Row className="main-grid-footer"></Row>
            </Container>
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

export { Main, Login };