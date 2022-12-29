import React from 'react';
import Layout from 'components/Layout';
import { useSelector } from 'react-redux';
import { Redirect } from 'react-router-dom';

const ProtectedRoutes = ({ children }) => {
  const { userAuthenticated } = useSelector((state) => state.userLoginReducer);
  if (!userAuthenticated) return <Redirect to="/login" />;

  return <Layout>{children}</Layout>;
};

export default ProtectedRoutes;
