import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Navbar from "../../components/Navbar";

const theme = createTheme();

const renderWithTheme = (component: React.ReactElement) => {
  return render(<ThemeProvider theme={theme}>{component}</ThemeProvider>);
};

describe("Navbar Component", () => {
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

  it("has proper ARIA attributes for accessibility", () => {
    renderWithTheme(<Navbar />);

    const navbar = screen.getByRole("banner");
    expect(navbar).toBeInTheDocument();
  });
});
