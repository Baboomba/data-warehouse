import { useState } from "react";
import { MENU_ITEM } from "../../../settings";
import './ListItem.css';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';


const SimpleItem = ({ menuitem }) => {
    const [whichPage, setWhichPage] = useState('');
    const handleClick = () => {
        setWhichPage(menuitem);
        console.log(menuitem);
    }
    return (
        <label className="menu-items">
            {MENU_ITEM[menuitem].icon}
            <span className="item-text" onClick={handleClick}>
                {MENU_ITEM[menuitem].name}
            </span>
        </label>
    );
};


const CollapseItem = ({ menuitem }) => {
    const [IsCollapsed, setIsCollapsed] = useState(false);
    
    const selectClassName = () => {
        if (IsCollapsed) {
            return 'sublist-open';
        } else {
            return 'sublist-close';
        }
    }

    const handleClick = () => {
        setIsCollapsed(!IsCollapsed);
    }

    const handleListItem = () => {
        return MENU_ITEM[menuitem].submenu.map(
                sub => <li className="submenu-items">{sub}</li>
        )            
    };

    return (
        <div>
            <label onClick={handleClick} className="menu-items">
                {MENU_ITEM[menuitem].icon}
                <span className="item-text">{MENU_ITEM[menuitem].name}</span>
                {IsCollapsed ?
                  <KeyboardArrowUpIcon className="list-arrow" /> :
                  <KeyboardArrowDownIcon className="list-arrow" />
                }
            </label>
            <ul className={selectClassName()}>
                {handleListItem()}
            </ul>
        </div>
    )
};


export { SimpleItem, CollapseItem }