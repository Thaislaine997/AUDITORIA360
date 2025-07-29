"""
Unit tests for src.core.validators module.
"""

import pytest

from src.core.validators import (
    validate_cpf, 
    validate_cnpj, 
    validate_email, 
    validate_required_fields,
    ValidationError
)


class TestValidateCPF:
    """Test cases for CPF validation."""

    def test_valid_cpf_with_formatting(self):
        """Test valid CPF with formatting (dots and dashes)."""
        assert validate_cpf("123.456.789-09") is True

    def test_valid_cpf_without_formatting(self):
        """Test valid CPF without formatting."""
        assert validate_cpf("12345678909") is True

    def test_invalid_cpf_wrong_length(self):
        """Test invalid CPF with wrong length."""
        assert validate_cpf("123456789") is False
        assert validate_cpf("123456789012") is False

    def test_invalid_cpf_all_same_digits(self):
        """Test invalid CPF with all same digits."""
        assert validate_cpf("11111111111") is False
        assert validate_cpf("000.000.000-00") is False

    def test_invalid_cpf_wrong_check_digits(self):
        """Test invalid CPF with wrong check digits."""
        assert validate_cpf("123.456.789-10") is False
        assert validate_cpf("12345678901") is False

    def test_invalid_cpf_empty_or_none(self):
        """Test invalid CPF with empty string or None."""
        assert validate_cpf("") is False
        assert validate_cpf(None) is False

    def test_invalid_cpf_non_string(self):
        """Test invalid CPF with non-string input."""
        assert validate_cpf(12345678909) is False
        assert validate_cpf([]) is False

    def test_invalid_cpf_with_letters(self):
        """Test invalid CPF with letters."""
        assert validate_cpf("abc.def.ghi-jk") is False
        assert validate_cpf("123.456.789-XX") is False


class TestValidateCNPJ:
    """Test cases for CNPJ validation."""

    def test_valid_cnpj_with_formatting(self):
        """Test valid CNPJ with formatting."""
        assert validate_cnpj("11.222.333/0001-81") is True

    def test_valid_cnpj_without_formatting(self):
        """Test valid CNPJ without formatting."""
        assert validate_cnpj("11222333000181") is True

    def test_invalid_cnpj_wrong_length(self):
        """Test invalid CNPJ with wrong length."""
        assert validate_cnpj("1122233300018") is False
        assert validate_cnpj("112223330001811") is False

    def test_invalid_cnpj_all_same_digits(self):
        """Test invalid CNPJ with all same digits."""
        assert validate_cnpj("11111111111111") is False
        assert validate_cnpj("00.000.000/0000-00") is False

    def test_invalid_cnpj_wrong_check_digits(self):
        """Test invalid CNPJ with wrong check digits."""
        assert validate_cnpj("11.222.333/0001-82") is False
        assert validate_cnpj("11222333000182") is False

    def test_invalid_cnpj_empty_or_none(self):
        """Test invalid CNPJ with empty string or None."""
        assert validate_cnpj("") is False
        assert validate_cnpj(None) is False

    def test_invalid_cnpj_non_string(self):
        """Test invalid CNPJ with non-string input."""
        assert validate_cnpj(11222333000181) is False
        assert validate_cnpj([]) is False


class TestValidateEmail:
    """Test cases for email validation."""

    def test_valid_email_simple(self):
        """Test valid simple email."""
        assert validate_email("test@example.com") is True

    def test_valid_email_with_subdomain(self):
        """Test valid email with subdomain."""
        assert validate_email("user@mail.example.com") is True

    def test_valid_email_with_plus(self):
        """Test valid email with plus sign."""
        assert validate_email("user+tag@example.com") is True

    def test_valid_email_with_numbers(self):
        """Test valid email with numbers."""
        assert validate_email("user123@example123.com") is True

    def test_invalid_email_missing_at(self):
        """Test invalid email missing @ symbol."""
        assert validate_email("userexample.com") is False

    def test_invalid_email_missing_domain(self):
        """Test invalid email missing domain."""
        assert validate_email("user@") is False

    def test_invalid_email_missing_tld(self):
        """Test invalid email missing top-level domain."""
        assert validate_email("user@example") is False

    def test_invalid_email_invalid_tld(self):
        """Test invalid email with invalid TLD."""
        assert validate_email("user@example.c") is False

    def test_invalid_email_empty_or_none(self):
        """Test invalid email with empty string or None."""
        assert validate_email("") is False
        assert validate_email(None) is False

    def test_invalid_email_non_string(self):
        """Test invalid email with non-string input."""
        assert validate_email(123) is False
        assert validate_email([]) is False


class TestValidateRequiredFields:
    """Test cases for required fields validation."""

    def test_valid_data_all_fields_present(self):
        """Test validation with all required fields present."""
        data = {"name": "John", "email": "john@example.com", "age": 30}
        required_fields = ["name", "email"]
        
        # Should not raise any exception
        validate_required_fields(data, required_fields)

    def test_missing_required_field(self):
        """Test validation with missing required field."""
        data = {"name": "John", "age": 30}
        required_fields = ["name", "email"]
        
        with pytest.raises(ValidationError, match="Missing required fields: email"):
            validate_required_fields(data, required_fields)

    def test_multiple_missing_required_fields(self):
        """Test validation with multiple missing required fields."""
        data = {"age": 30}
        required_fields = ["name", "email", "phone"]
        
        with pytest.raises(ValidationError, match="Missing required fields"):
            validate_required_fields(data, required_fields)

    def test_empty_string_field(self):
        """Test validation with empty string field."""
        data = {"name": "", "email": "john@example.com"}
        required_fields = ["name", "email"]
        
        with pytest.raises(ValidationError, match="Empty required fields: name"):
            validate_required_fields(data, required_fields)

    def test_whitespace_only_field(self):
        """Test validation with whitespace-only field."""
        data = {"name": "   ", "email": "john@example.com"}
        required_fields = ["name", "email"]
        
        with pytest.raises(ValidationError, match="Empty required fields: name"):
            validate_required_fields(data, required_fields)

    def test_none_field_value(self):
        """Test validation with None field value."""
        data = {"name": None, "email": "john@example.com"}
        required_fields = ["name", "email"]
        
        with pytest.raises(ValidationError, match="Empty required fields: name"):
            validate_required_fields(data, required_fields)

    def test_zero_as_valid_field(self):
        """Test that zero is considered a valid field value."""
        data = {"score": 0, "name": "John"}
        required_fields = ["score", "name"]
        
        # Should not raise any exception
        validate_required_fields(data, required_fields)

    def test_false_as_valid_field(self):
        """Test that False is considered a valid field value."""
        data = {"active": False, "name": "John"}
        required_fields = ["active", "name"]
        
        # Should not raise any exception
        validate_required_fields(data, required_fields)

    def test_empty_required_fields_list(self):
        """Test validation with empty required fields list."""
        data = {"name": "John"}
        required_fields = []
        
        # Should not raise any exception
        validate_required_fields(data, required_fields)