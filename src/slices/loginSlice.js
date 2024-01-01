import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export const loginAsync = createAsyncThunk('/login', async ({ email, password }) => {
    const url = 'http://localhost:8000/api/login/';
    const data = { email, password };
    const response = await axios.post(url, data, { withCredentials: true });
    return response.data.data.refresh;
});

const initialState = {
    isLoggedIn: false,
    refresh: null,
};

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logIn: (state) => { state.isLoggedIn = true; },
        logOut: (state) => { state.isLoggedIn = false; },
        setRefresh: (state, action) => { state.refresh = action.payload; },
    },
    extraReducers: (builder) => {
        builder
            .addCase(loginAsync.fulfilled, (state, action) => {
                state.refresh = action.payload;
                state.isLoggedIn = true;
            })
            .addCase(loginAsync.rejected, (state, action) => {
                console.error('Login failed: ', action.error);
            });
    },
});

export const { logIn, logOut } = authSlice.actions;
export default authSlice.reducer;