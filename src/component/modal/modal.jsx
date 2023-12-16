import './Modal.css';

const ListModal = ({ onClicked }) => {
    return (
        <div
          className={
            onClicked ?
            'list-modal-container' :
            'list-modal-container-hidden'
          }
        >
        </div>
    );
};

export { ListModal };