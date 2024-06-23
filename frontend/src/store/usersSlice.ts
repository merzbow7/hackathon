import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import http from '../services/http';

export interface User {
  id: number;
  telegram_id: number;
  telegram_username: string;
  first_name: string;
  last_name: string;
  keycloak_id: string;
  verification_code: string;
  institution: {
    id: number;
    name: string;
  };
  enabled: boolean;
}

export interface UserState {
  items: Array<User>;
  loading: boolean;
  error: unknown;
}

const initialState: UserState = {
  items: [],
  loading: false,
  error: null,
};


const fetchUsers = createAsyncThunk(
  'users/fetchUsers',
  async () => {
    const response = await http.get('/admin/users');
    return response.data;
  }
);

const deleteUser = createAsyncThunk(
  'users/deleteUser',
  async (userId: string | number) => {
    await http.delete(`/admin/user/${userId}`);
  }
);

const updateInstitution = createAsyncThunk(
  'users/updateInstitution',
  async (params: {userId: string | number, institutionId: string}, { dispatch }) => {
    await http.put(`/admin/user/${params.userId}`, {
      institution_id: params.institutionId
    });
    dispatch(fetchUsers());
  }
);

const counterSlice = createSlice({
  name: "users",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
  },
});

export {
  fetchUsers,
  deleteUser,
  updateInstitution,
};

export default counterSlice.reducer;