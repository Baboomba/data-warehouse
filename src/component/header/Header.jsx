import { Col, Container } from 'react-bootstrap';
import './Headers.css';




const Headers = () => {
    return (
        <div>
            <Container fluid>
                <Col className='header-leftside'>left</Col>
                <Col className='header-rightside'>right</Col>
            </Container>
        </div>
    );
};

export { Headers };