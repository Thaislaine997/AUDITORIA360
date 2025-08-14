// Arquivo de teste zerado para build limpa
// Arquivo de teste zerado para build limpa
// Arquivo de teste zerado para build limpa
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Sidebar from "../../components/Sidebar";

const theme = createTheme();

// Mock react-router-dom
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

describe("Sidebar Component - Simple Tests", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it("renders without crashing", () => {
    renderWithProviders(<Sidebar />);
    expect(document.body).toBeInTheDocument();
  });

  it("displays dashboard menu item", () => {
    renderWithProviders(<Sidebar />);
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
  });

  it("displays all main menu items", () => {
    renderWithProviders(<Sidebar />);

    const menuItems = [
      "Dashboard",
      "Folha de Pagamento",
      "Documentos",
      "CCT",
      "Auditoria",
      "Chatbot",
    ];

    menuItems.forEach(item => {
      expect(screen.getByText(item)).toBeInTheDocument();
    });
  });

  it("calls navigate when clicking on a menu item", () => {
    renderWithProviders(<Sidebar />);

    const auditItem = screen.getByText("Auditoria");
    fireEvent.click(auditItem);

    expect(mockNavigate).toHaveBeenCalledWith("/audit");
  });
});
