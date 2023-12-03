import { Logo } from "./logo/Logo";
import MenuList from "./menuList/MenuList";
import './SideMenu.css';

const SideMenu = () => {
    return (
        <div className="side-menu-bg">
            <Logo />
            <MenuList />
        </div>
    );
};

export default SideMenu;