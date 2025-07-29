import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Sidebar from "../../components/Sidebar";

const theme = createTheme();

// Mock react-router-dom hooks
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
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
  });

  it("renders all menu items", () => {
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

    const dashboardItem = screen.getByText("Dashboard").closest("button");
    expect(dashboardItem).toHaveClass("Mui-selected");
  });

  it("navigates to correct route when menu item is clicked", () => {
    renderWithProviders(<Sidebar />);

    const payrollItem = screen.getByText("Folha de Pagamento");
    fireEvent.click(payrollItem);

    expect(mockNavigate).toHaveBeenCalledWith("/payroll");
  });

  it("renders with correct drawer width", () => {
    renderWithProviders(<Sidebar />);

    const drawer = screen.getByRole("presentation");
    expect(drawer).toBeInTheDocument();
  });

  it("displays menu items with icons", () => {
    renderWithProviders(<Sidebar />);

    // Check that all menu items are rendered
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Folha de Pagamento")).toBeInTheDocument();
    expect(screen.getByText("Documentos")).toBeInTheDocument();
    expect(screen.getByText("CCT")).toBeInTheDocument();
    expect(screen.getByText("Auditoria")).toBeInTheDocument();
    expect(screen.getByText("Chatbot")).toBeInTheDocument();
  });
});
