import { createTheme } from '@mui/material/styles';

// Design tokens
const tokens = {
  colors: {
    primary: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3',
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
    secondary: {
      50: '#f3e5f5',
      100: '#e1bee7',
      200: '#ce93d8',
      300: '#ba68c8',
      400: '#ab47bc',
      500: '#9c27b0',
      600: '#8e24aa',
      700: '#7b1fa2',
      800: '#6a1b9a',
      900: '#4a148c',
    },
    success: {
      50: '#e8f5e8',
      100: '#c8e6c9',
      200: '#a5d6a7',
      300: '#81c784',
      400: '#66bb6a',
      500: '#4caf50',
      600: '#43a047',
      700: '#388e3c',
      800: '#2e7d32',
      900: '#1b5e20',
    },
    warning: {
      50: '#fff8e1',
      100: '#ffecb3',
      200: '#ffe082',
      300: '#ffd54f',
      400: '#ffca28',
      500: '#ffc107',
      600: '#ffb300',
      700: '#ffa000',
      800: '#ff8f00',
      900: '#ff6f00',
    },
    error: {
      50: '#ffebee',
      100: '#ffcdd2',
      200: '#ef9a9a',
      300: '#e57373',
      400: '#ef5350',
      500: '#f44336',
      600: '#e53935',
      700: '#d32f2f',
      800: '#c62828',
      900: '#b71c1c',
    },
    grey: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#eeeeee',
      300: '#e0e0e0',
      400: '#bdbdbd',
      500: '#9e9e9e',
      600: '#757575',
      700: '#616161',
      800: '#424242',
      900: '#212121',
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
  },
  shadows: {
    sm: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
    md: '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)',
    lg: '0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)',
    xl: '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)',
  },
  transitions: {
    fast: '150ms ease-in-out',
    normal: '250ms ease-in-out',
    slow: '350ms ease-in-out',
  },
};

// Light theme
export const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: tokens.colors.primary[600],
      light: tokens.colors.primary[400],
      dark: tokens.colors.primary[800],
      contrastText: '#ffffff',
    },
    secondary: {
      main: tokens.colors.secondary[600],
      light: tokens.colors.secondary[400],
      dark: tokens.colors.secondary[800],
      contrastText: '#ffffff',
    },
    success: {
      main: tokens.colors.success[600],
      light: tokens.colors.success[400],
      dark: tokens.colors.success[800],
    },
    warning: {
      main: tokens.colors.warning[600],
      light: tokens.colors.warning[400],
      dark: tokens.colors.warning[800],
    },
    error: {
      main: tokens.colors.error[600],
      light: tokens.colors.error[400],
      dark: tokens.colors.error[800],
    },
    background: {
      default: tokens.colors.grey[50],
      paper: '#ffffff',
      card: '#ffffff',
      sidebar: tokens.colors.grey[100],
    },
    text: {
      primary: tokens.colors.grey[900],
      secondary: tokens.colors.grey[700],
      disabled: tokens.colors.grey[500],
    },
    divider: tokens.colors.grey[200],
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h6: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 600,
      textTransform: 'none',
    },
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.4,
    },
  },
  shape: {
    borderRadius: parseInt(tokens.borderRadius.md),
  },
  spacing: (factor) => `${factor * 8}px`,
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: tokens.borderRadius.md,
          padding: `${tokens.spacing.sm} ${tokens.spacing.lg}`,
          transition: tokens.transitions.normal,
          boxShadow: tokens.shadows.sm,
          '&:hover': {
            boxShadow: tokens.shadows.md,
            transform: 'translateY(-1px)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: tokens.shadows.md,
          },
        },
        outlined: {
          borderWidth: '2px',
          '&:hover': {
            borderWidth: '2px',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: tokens.borderRadius.lg,
          boxShadow: tokens.shadows.sm,
          transition: tokens.transitions.normal,
          '&:hover': {
            boxShadow: tokens.shadows.md,
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: tokens.borderRadius.md,
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: tokens.borderRadius.md,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: tokens.borderRadius.md,
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          boxShadow: tokens.shadows.md,
          '&:hover': {
            boxShadow: tokens.shadows.lg,
          },
        },
      },
    },
  },
});

// Dark theme
export const darkTheme = createTheme({
  ...lightTheme,
  palette: {
    mode: 'dark',
    primary: {
      main: tokens.colors.primary[400],
      light: tokens.colors.primary[300],
      dark: tokens.colors.primary[600],
      contrastText: '#000000',
    },
    secondary: {
      main: tokens.colors.secondary[400],
      light: tokens.colors.secondary[300],
      dark: tokens.colors.secondary[600],
      contrastText: '#000000',
    },
    success: {
      main: tokens.colors.success[400],
      light: tokens.colors.success[300],
      dark: tokens.colors.success[600],
    },
    warning: {
      main: tokens.colors.warning[400],
      light: tokens.colors.warning[300],
      dark: tokens.colors.warning[600],
    },
    error: {
      main: tokens.colors.error[400],
      light: tokens.colors.error[300],
      dark: tokens.colors.error[600],
    },
    background: {
      default: tokens.colors.grey[900],
      paper: tokens.colors.grey[800],
      card: tokens.colors.grey[800],
      sidebar: tokens.colors.grey[850],
    },
    text: {
      primary: tokens.colors.grey[100],
      secondary: tokens.colors.grey[300],
      disabled: tokens.colors.grey[600],
    },
    divider: tokens.colors.grey[700],
  },
  components: {
    ...lightTheme.components,
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: tokens.borderRadius.lg,
          boxShadow: `0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.4)`,
          transition: tokens.transitions.normal,
          '&:hover': {
            boxShadow: `0 3px 6px rgba(0,0,0,0.4), 0 3px 6px rgba(0,0,0,0.5)`,
          },
        },
      },
    },
  },
});

export { tokens };
