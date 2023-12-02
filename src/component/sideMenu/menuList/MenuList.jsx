import { CollapseItem, SimpleItem } from "../listItem/ListItem";
import { MENU_ITEM } from "../../../settings";



const CreateList = () => {
    const items = Object.keys(MENU_ITEM);
    return items.map(item => (
        <li key={item} className="li-items">
            {
                MENU_ITEM[item].collapse ?
                <CollapseItem menuname={MENU_ITEM[item].name} /> :
                <SimpleItem menuname={MENU_ITEM[item].name} />
            }
        </li>
    ))
};

const MenuList = () => {
    return (
        <div>
            <ul>
                {CreateList()}
            </ul>
        </div>
    );
};


export default MenuList;