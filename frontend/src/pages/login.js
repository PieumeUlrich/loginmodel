import Head from 'next/head';
import NextLink from 'next/link';
import { useRouter } from 'next/router';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import { Box, Button, Container, Grid, Link, TextField, Typography, Checkbox } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { Facebook as FacebookIcon } from '../icons/facebook';
import { Google as GoogleIcon } from '../icons/google';
import { proxy } from 'src/utils/setupProxy';
import useToken from '/src/utils/useToken';
import {userService} from './../services/user.service'
import { useEffect } from 'react'
// import { login } from 'src/utils/auth';


const Login = () => {
  const router = useRouter();
  const { token, setToken } = useToken()
  useEffect(() => {
    // Prefetch the dashboard page
      if(router.query.returnUrl) router.prefetch(router.query.returnUrl)
      else router.prefetch('/dashboard')
  }, [])  
  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
      remember: true
    },
    validationSchema: Yup.object({
      email: Yup
        .string()
        .email(
          'Must be a valid email')
        .max(255)
        .required(
          'Email is required'),
      password: Yup
        .string()
        .max(255)
        .required(
          'Password is required'),
      remeber: Yup
      .boolean()
      .oneOf(
        [false],
      )
      }),
    onSubmit: () => {
      const data = {
        email: formik.values.email,
        password: formik.values.password,
        remember: formik.values.remember
      }
      loginUser(data)
      // const opts = {
      //   method: "POST",
      //   headers: {
      //     'content-type': 'application/json',
      //   },
      //   body: JSON.stringify(data)
      // }
      // fetch(`${proxy}/auth/login`, opts)
      // .then(send => send.json())
      // .then(res => {
      //   if(res[1].status === 201){
      //     // login(res[1].access_token)
      //     // localStorage.setItem('userId', res[1].userId);
      //     // localStorage.setItem('token', res[1].access_token);
      //     setToken(res[1].access_token)
      //     alert(res[0].msg)
      //     router.push('/dashboard');
      //   }
      //   else {
      //     formik.values.email = ""
      //     formik.values.password = ""
      //     alert(res[0].msg)
      //   }
      // })
      // .catch(err => console.error(err.msg))
    }
  });

  function loginUser(data) {
    return userService.login(data)
      .then((res) => {
        if(res[1].status === 201){
          localStorage.setItem('user', JSON.stringify(res[1].user));
          localStorage.setItem('token', JSON.stringify(res[1].access_token));
          alert(res[0].msg)
          if(router.query.returnUrl){
            router.push(router.query.returnUrl)
          }
          else router.push('/dashboard')
        }
        else {
          alert(res[0].msg)
        }
      })
      .catch(err => err.msg);
  }
  return (
    <>
      <Head>
        <title>Login | Material Kit</title>
      </Head>
      <Box
        component="main"
        sx={{
          alignItems: 'center',
          display: 'flex',
          flexGrow: 1,
          minHeight: '100%'
        }}
      >
        <Container maxWidth="sm">
          <NextLink
            href="/"
            passHref
          >
            <Button
              component="a"
              startIcon={<ArrowBackIcon fontSize="small" />}
            >
              Dashboard
            </Button>
          </NextLink>
          <form onSubmit={formik.handleSubmit}>
            <Box sx={{ my: 3 }}>
              <Typography
                color="textPrimary"
                variant="h4"
              >
                Sign in
              </Typography>
              <Typography
                color="textSecondary"
                gutterBottom
                variant="body2"
              >
                Sign in on the internal platform
              </Typography>
            </Box>
            {/* <Grid
              container
              spacing={3}
            >
              <Grid
                item
                xs={12}
                md={6}
              >
                <Button
                  color="info"
                  fullWidth
                  startIcon={<FacebookIcon />}
                  onClick={formik.handleSubmit}
                  size="large"
                  variant="contained"
                >
                  Login with Facebook
                </Button>
              </Grid>
              <Grid
                item
                xs={12}
                md={6}
              >
                <Button
                  fullWidth
                  color="error"
                  startIcon={<GoogleIcon />}
                  onClick={formik.handleSubmit}
                  size="large"
                  variant="contained"
                >
                  Login with Google
                </Button>
              </Grid>
            </Grid>
            <Box
              sx={{
                pb: 1,
                pt: 3
              }}
            >
              <Typography
                align="center"
                color="textSecondary"
                variant="body1"
              >
                or login with email address
              </Typography>
            </Box> */}
            <TextField
              error={Boolean(formik.touched.email && formik.errors.email)}
              fullWidth
              helperText={formik.touched.email && formik.errors.email}
              label="Email Address"
              margin="normal"
              name="email"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              type="email"
              value={formik.values.email}
              variant="outlined"
            />
            <TextField
              error={Boolean(formik.touched.password && formik.errors.password)}
              fullWidth
              helperText={formik.touched.password && formik.errors.password}
              label="Password"
              margin="normal"
              name="password"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              type="password"
              value={formik.values.password}
              variant="outlined"
            />
            <Box
              sx={{
                alignItems: 'center',
                display: 'flex',
                ml: -1
              }}
            >
              <Checkbox
                checked={formik.values.remember}
                name="remember"
                onChange={formik.handleChange}
              />
              <Typography
                color="textSecondary"
                variant="body2"
              >
                Remember Me
              </Typography>
            </Box>
            {Boolean(formik.touched.remember)}
            <Box sx={{ py: 2 }}>
              <Button
                color="primary"
                // disabled={formik.isSubmitting}
                fullWidth
                size="large"
                type="submit"
                variant="contained"
              >
                Sign In Now
              </Button>
            </Box>
            <Typography
              color="textSecondary"
              variant="body2"
            >
              Don&apos;t have an account?
              {' '}
              <NextLink
                href="/register"
              >
                <Link
                  to="/register"
                  variant="subtitle2"
                  underline="hover"
                  sx={{
                    cursor: 'pointer'
                  }}
                >
                  Sign Up
                </Link>
              </NextLink>
            </Typography>
          </form>
        </Container>
      </Box>
    </>
  );
};

export default Login;
