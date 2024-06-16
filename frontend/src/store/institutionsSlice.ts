import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import http from '../services/http';

export interface Institution {
  id: number;
  name: string;
}

export interface InstitutionState {
  items: Array<Institution>;
  mounted: boolean;
  loading: boolean;
  error: unknown;
}

const initialState: InstitutionState = {
  items: [],
  mounted: false,
  loading: false,
  error: null,
};


const fetchInstitutions = createAsyncThunk(
  'institutions/fetchInstitutions',
  async () => {
    const response = await http.get('/admin/institutions');
    return response.data;
  }
);

const addInstitution = createAsyncThunk(
  'institutions/addInstitution',
  async (name, { dispatch }) => {
    await http.post(`/admin/add_institution?group_name=${name}`);
    dispatch(fetchInstitutions());
  }
);

const institutionsSlice = createSlice({
  name: "institutions",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInstitutions.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
        state.mounted = true;
      })
      .addCase(fetchInstitutions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchInstitutions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      .addCase(addInstitution.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(addInstitution.pending, (state) => {
        state.loading = true;
      })
      .addCase(addInstitution.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
  },
});

export {
  fetchInstitutions,
  addInstitution,
};

export default institutionsSlice.reducer;