import BarChartIcon from '@mui/icons-material/BarChart';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import StorageIcon from '@mui/icons-material/Storage';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';


const MENU_ITEM = {
    item1 : {
        name : 'BASIC TABLE',
        icon : <TextSnippetIcon />,
        collapse : true,
        submenu : [
            'product',
            'model',
            'promotion',
            'category'
        ],
        path : '/basic-table'
    },

    item2 : {
        name : 'ALALYSIS',
        icon : <BarChartIcon />,
        collapse : true,
        submenu : [
            'sub a',
            'sub b',
            'sub c',
            'sub d'
        ],
        path : '/analysis'
    },

    item3 : {
        name : 'DATABASE',
        icon: <StorageIcon />,
        collapse : true,
        submenu : [
            'samsung',
            'toss',
            'insurance'
        ]
    },

    item4 : {
        name : 'ACCOUNT',
        icon : <AccountCircleIcon />,
        collapse : false,
        submenu : null
    }
};


export { MENU_ITEM };