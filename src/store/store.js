import { configureStore } from '@reduxjs/toolkit';
import { authSlice } from '../slices/loginSlice';
import { menuSlice } from '../slices/pageSlice';


const rootReducer = {
    auth: authSlice.reducer,
    menu: menuSlice.reducer,
}


export const store = configureStore({
    reducer: rootReducer,
});