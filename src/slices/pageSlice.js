import { createSlice } from '@reduxjs/toolkit';


export const menuSlice = createSlice({
    name: 'menu',
    initialState: {
        selectedMenu: 'home',
    },
    reducers: {
        selectedMenu: (state, action) => {
            state.selectedMenu = action.payload;
        },
    },
});

export const { selectedMenu } = menuSlice.actions;
export default menuSlice.reducer;