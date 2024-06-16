import usersReducer from "./usersSlice";
import accountReducer from "./accountSlice";
import institutionsReducer from './institutionsSlice';
import { configureStore } from "@reduxjs/toolkit";
import { useDispatch, useSelector, type TypedUseSelectorHook, } from 'react-redux';

const reducer = {
  users: usersReducer,
  account: accountReducer,
  institutions: institutionsReducer
};

const store = configureStore({
  reducer,
});

export const useAppDispatch: () => typeof store.dispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<ReturnType<typeof store.getState>> = useSelector;

export default store;