import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import PhuComponent from 'screens/VoiceMailReview';
import Login from 'screens/Login';
import ProtectedRoutes from 'components/ProtectedRoutes';
import { createTheme, ThemeProvider } from '@material-ui/core';
import LoaderComponent from 'components/Loader';

const theme = createTheme({
  palette: {
    primary: { main: '#1464DF', contrastText: '#ffffff' },
    white: { main: '#ffffff', secondary: '#f8fbff' },
    common: {
      muted: '#797575',
    },
  },
  typography: { fontSize: 12 },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router basename={process.env.REACT_APP_NAME}>
        <div className="App">
          <LoaderComponent />
          <Switch>
            <Route exact path="/login" component={Login} />
            <ProtectedRoutes>
              <Route path={`/(|voicemail)`} component={PhuComponent} />
            </ProtectedRoutes>
          </Switch>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
