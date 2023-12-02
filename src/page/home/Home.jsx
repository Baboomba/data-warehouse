import { Container, Row, Col } from "react-bootstrap";
import './Home.css';
import { LoginForm } from "../login/Login";
import SideMenu from "../../component/sideMenu/SideMenu";


const Main = () => {
    return (
        <div>
            <Container fluid>
                <Row>
                    <Col xxl={2} className="main-grid-left">
                        <SideMenu />
                    </Col>
                    <Col className="main-grid-right">
                        <Row className="main-grid-header">Main Header
                        </Row>
                        <Row className="main-grid-content">Content
                        </Row>
                    </Col>
                </Row>
                <Row className="main-grid-footer">footer</Row>
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