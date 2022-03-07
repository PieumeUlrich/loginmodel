import Head from 'next/head';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { CacheProvider } from '@emotion/react';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import { CssBaseline } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { createEmotionCache } from '../utils/create-emotion-cache';
import { theme } from '../theme';

const clientSideEmotionCache = createEmotionCache();

const App = (props) => {
  const [authorized, setAuthorized] = useState(false)
  const [user, setUser] = useState(null)
  const router = useRouter()
  const userLogged = process.browser && JSON.parse(localStorage.getItem('user'))
  
  useEffect(() => {
    // on initial load - run auth check 
    authCheck(router.asPath);
    // on route change start - hide page content by setting authorized to false  
    const hideContent = () => setAuthorized(false);
    router.events.on('routeChangeStart', hideContent);

    // on route change complete - run auth check 
    router.events.on('routeChangeComplete', authCheck)

    // unsubscribe from events in useEffect return function
    return () => {
      router.events.off('routeChangeStart', hideContent);
      router.events.off('routeChangeComplete', authCheck);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

const authCheck = (url) => {
    // redirect to login page if accessing a private page and not logged in 
    const publicPaths = ['/','/login', '/register'];
    const path = url.split('?')[0];
    if (!userLogged && !publicPaths.includes(path)) {
        setAuthorized(false);
        router.push({
            pathname: '/login',
            query: { returnUrl: router.asPath }
        });
    } else {
        setAuthorized(true);
    }
}  
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;
  const getLayout = Component.getLayout ?? ((page) => page);
return (
    <CacheProvider value={emotionCache}>
      <Head>
        <title>
          Material Kit Pro
        </title>
        <meta
          name="viewport"
          content="initial-scale=1, width=device-width"
        />
      </Head>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {authorized && getLayout(<Component {...pageProps} />)}
        </ThemeProvider>
      </LocalizationProvider>
    </CacheProvider>
  );
};

export default App;
