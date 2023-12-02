import { useState } from "react";
import { MENU_ITEM } from "../../../settings";

const SimpleItem = ({ menuname }) => {
    return (
        <label>{menuname}</label>
    );
};


const CollapseItem = ({ menuname }) => {
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

    const condition = (item) => {
        if (MENU_ITEM[item].collapse)
        {
            return MENU_ITEM[item].submenu.map(
                sub => <li>{sub}</li>
            )
        }
    };

    const handleListItem = () => {
        const items = Object.keys(MENU_ITEM);
        
        return items.map(item => condition(item));
    };

    return (
        <div>
            <label>{menuname}</label>
            <ul className={selectClassName()} onClick={handleClick}>
                {handleListItem()}
            </ul>
        </div>
    )
};


export { SimpleItem, CollapseItem }