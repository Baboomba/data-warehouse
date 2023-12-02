const MENU_ITEM = {
    item1 : {
        name : 'item a',
        collapse : false,
        submenu : null
    },
    item2 : {
        name : 'item b',
        collapse : false,
        submenu : null
    },
    item3 : {
        name : 'item c',
        collapse : true,
        submenu : [
            'sub a',
            'sub b',
            'sub c',
            'sub d'
        ]
    },
    item4 : {
        name : 'item d',
        collapse : false,
        submenu : null
    }
};

export { MENU_ITEM };