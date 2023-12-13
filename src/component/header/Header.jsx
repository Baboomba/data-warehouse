import { Col, Container } from 'react-bootstrap';
import './Header.css';




const Header = () => {
    return (
        <div className='header-container'>
            <Container fluid>
                <Col className='header-leftside'>left</Col>
                <Col className='header-rightside'>right</Col>
            </Container>
        </div>
    );
};

export { Header };