import { describe, it, expect, beforeEach } from "@jest/globals";
import { render, screen } from "@testing-library/react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Navbar from "../../components/layout/Navbar";
import { useUIStore } from "../../stores/uiStore";
import { useAuthStore } from "../../stores/authStore";

const theme = createTheme();

const renderWithTheme = (component: React.ReactElement) => {
  return render(<ThemeProvider theme={theme}>{component}</ThemeProvider>);
};

describe("Navbar Component", () => {
  beforeEach(() => {
    // Reset stores
    useUIStore.setState({
      sidebarOpen: true,
      currentPage: "/dashboard",
      notifications: [],
    });
    useAuthStore.setState({
      user: {
        id: "1",
        name: "Test User",
        email: "test@example.com",
        role: "admin",
        permissions: [],
      },
      isAuthenticated: true,
      loading: false,
      permissions: [],
    });
  });

  it("renders the navbar with correct title", () => {
    renderWithTheme(<Navbar />);

    expect(
      screen.getByText("AUDITORIA360 - Portal de Gestão da Folha")
    ).toBeInTheDocument();
  });

  it("renders as an AppBar with fixed position", () => {
    renderWithTheme(<Navbar />);

    const navbar = screen.getByRole("banner");
    expect(navbar).toBeInTheDocument();
  });

  it("displays the title with correct typography variant", () => {
    renderWithTheme(<Navbar />);

    const title = screen.getByText("AUDITORIA360 - Portal de Gestão da Folha");
    expect(title).toHaveClass("MuiTypography-h6");
  });

  it("has sidebar toggle button", () => {
    renderWithTheme(<Navbar />);

    const toggleButton = screen.getByLabelText("toggle sidebar");
    expect(toggleButton).toBeInTheDocument();
  });

  it("has user account menu button", () => {
    renderWithTheme(<Navbar />);

    const accountButton = screen.getByLabelText("account menu");
    expect(accountButton).toBeInTheDocument();
  });
});
