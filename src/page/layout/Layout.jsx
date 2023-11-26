import { Container, Row, Col } from "react-bootstrap";
import './Layout.css';

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
            <Container>

            </Container>
        </div>
    );
};

export { Main, Login };