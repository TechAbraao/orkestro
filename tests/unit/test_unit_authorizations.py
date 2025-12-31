from source.app.services.authorizations_services import AuthorizationsServices
from source.app.exceptions.stores_exceptions import StoresNotFoundException
from source.app.exceptions.authorizations_exceptions import InvalidPasswordException
from unittest.mock import patch, MagicMock
import pytest
import logging

class TestUnitAuthorizations:
    @classmethod
    def setup_class(cls):
        logging.disable(logging.CRITICAL)

    @patch("source.app.services.authorizations_services.StoresRepository")
    def test_verify_store_credentials_store_not_found(self, mock_repo_class):
        mock_repo = MagicMock()
        mock_repo.find_by_email.return_value = None

        mock_repo_class.return_value = mock_repo
        authorizations_services = AuthorizationsServices()

        with pytest.raises(StoresNotFoundException) as exc_info:
            authorizations_services.verify_store_credentials(
                "email@test.com",
                "123456"
            )

        assert str(exc_info.value) == "Comércio não encontrado."


        mock_repo.find_by_email.assert_called_once_with("email@test.com")


    @patch("source.app.services.authorizations_services.verify_password")
    @patch("source.app.services.authorizations_services.StoresRepository")
    def test_verify_store_credentials_invalid_password(self, mock_repo_class, mock_verify_password):
        mock_store = MagicMock()
        mock_store.password = "hashed_password"
        mock_store.serialize = {"id": 1}

        mock_repo_class.return_value.find_by_email.return_value = mock_store

        mock_verify_password.return_value = False

        service = AuthorizationsServices()

        with pytest.raises(InvalidPasswordException):
            service.verify_store_credentials("email@test.com", "wrong_password")

        mock_repo_class.return_value.find_by_email.assert_called_once_with("email@test.com")
        mock_verify_password.assert_called_once_with(password="wrong_password", hashed_password="hashed_password")
