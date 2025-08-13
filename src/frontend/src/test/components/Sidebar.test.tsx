import { describe, it, expect, beforeEach, jest } from "@jest/globals";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Sidebar from "../../components/layout/Sidebar";
import { useUIStore } from "../../stores/uiStore";

const theme = createTheme();

// Mock react-router-dom hooks
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => {
  const actual = jest.requireActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
    useLocation: () => ({ pathname: "/dashboard" }),
  };
});

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>{component}</ThemeProvider>
    </BrowserRouter>
  );
};

describe("Sidebar Component", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    // Reset UI store state
    useUIStore.setState({
      sidebarOpen: true,
      currentPage: "/dashboard",
      notifications: [],
    });
  });

  it("renders all menu items when sidebar is open", () => {
    renderWithProviders(<Sidebar />);

    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Folha de Pagamento")).toBeInTheDocument();
    expect(screen.getByText("Documentos")).toBeInTheDocument();
    expect(screen.getByText("CCT")).toBeInTheDocument();
    expect(screen.getByText("Auditoria")).toBeInTheDocument();
    expect(screen.getByText("Chatbot")).toBeInTheDocument();
  });

  it("highlights the active menu item", () => {
    renderWithProviders(<Sidebar />);

    const dashboardItem = screen.getByText("Dashboard").closest("a");
    expect(dashboardItem).toHaveClass("Mui-selected");
  });

  it("navigates to correct route when menu item is clicked", () => {
    renderWithProviders(<Sidebar />);

    const payrollItem = screen.getByText("Folha de Pagamento");
    fireEvent.click(payrollItem);

    expect(mockNavigate).toHaveBeenCalledWith("/payroll");
  });

  it("does not render menu items when sidebar is closed", () => {
    // Close the sidebar
    useUIStore.setState({ sidebarOpen: false });
    
    renderWithProviders(<Sidebar />);

    // Menu items should not be visible when sidebar is closed
    expect(screen.queryByText("Dashboard")).not.toBeInTheDocument();
  });

  it("displays menu items with correct accessibility attributes", () => {
    renderWithProviders(<Sidebar />);

    const dashboardLink = screen.getByLabelText("Navegar para Dashboard");
    expect(dashboardLink).toBeInTheDocument();
  });
});
