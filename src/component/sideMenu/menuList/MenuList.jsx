import { CollapseItem, SimpleItem } from "../listItem/ListItem";
import { MENU_ITEM } from "../../../settings";
import './MenuList.css';


const CreateList = () => {
    const items = Object.keys(MENU_ITEM);
    return items.map(item => (
        <li key={item} className="main-menu-list-item">
            {
                MENU_ITEM[item].collapse ?
                <CollapseItem menuitem={item} /> :
                <SimpleItem menuitem={item} />
            }
        </li>
    ))
};

const MenuList = () => {
    return (
        <div className="main-menu-bg">
            <ul className="main-menu-list" >
                {CreateList()}
            </ul>
            <div className="scroll-cover"></div>
        </div>
    );
};


export default MenuList;