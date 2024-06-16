import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import http from '../services/http';

export interface AccountState {
  isBind: boolean;
  loading: boolean;
  error: string | null;
}

const initialState: AccountState = {
  isBind: false,
  loading: true,
  error: null,
};

const bindUser = createAsyncThunk(
  'account/bindUser',
  async (code) => {
    const response = await http.get(`/auth/registration?code=${code}`);
    return response.data;
  }
);

const accountSlice = createSlice({
  name: "account",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(bindUser.fulfilled, (state) => {
      state.isBind = true;
      state.loading = false;
    })
    .addCase(bindUser.pending, (state) => {
      state.loading = true;
    })
    .addCase(bindUser.rejected, (state) => {
      state.loading = false;
      state.error = 'Что то пошло не так, обратитесь к администратору!';
    })
  },
});

export {
  bindUser,
};

export default accountSlice.reducer;