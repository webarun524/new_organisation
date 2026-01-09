import pytest

from shared.bitbucket.get_token_from_envs import get_token_from_envs


class TestGetTokenFromEnvs:
    """Test suite for get_token_from_envs function"""

    def test_get_token_success(self, monkeypatch):
        """Test successful token retrieval from environment variable"""
        token = "valid_bitbucket_token_12345"
        monkeypatch.setenv("BITBUCKET_TOKEN", token)

        result = get_token_from_envs()

        assert result == token

    def test_get_token_with_whitespace(self, monkeypatch):
        """Test token retrieval with leading/trailing whitespace"""
        token = "valid_bitbucket_token_12345"
        monkeypatch.setenv("BITBUCKET_TOKEN", f"  {token}  ")

        result = get_token_from_envs()

        assert result == token
        assert result == result.strip()

    def test_get_token_missing_env_var(self, monkeypatch):
        """Test error when BITBUCKET_TOKEN environment variable is not set"""
        monkeypatch.delenv("BITBUCKET_TOKEN", raising=False)

        with pytest.raises(ValueError) as exc_info:
            get_token_from_envs()

        assert "Missing required environment variable: BITBUCKET_TOKEN" in str(
            exc_info.value
        )

    def test_get_token_empty_env_var(self, monkeypatch):
        """Test error when BITBUCKET_TOKEN environment variable is empty"""
        monkeypatch.setenv("BITBUCKET_TOKEN", "")

        with pytest.raises(ValueError) as exc_info:
            get_token_from_envs()

        assert "BITBUCKET_TOKEN cannot be empty" in str(exc_info.value)

    def test_get_token_whitespace_only(self, monkeypatch):
        """Test error when BITBUCKET_TOKEN contains only whitespace"""
        monkeypatch.setenv("BITBUCKET_TOKEN", "   ")

        with pytest.raises(ValueError) as exc_info:
            get_token_from_envs()

        assert "BITBUCKET_TOKEN cannot be empty" in str(exc_info.value)

    def test_get_token_different_tokens(self, monkeypatch):
        """Test that changing environment variable between calls returns different tokens"""
        token1 = "first_token"
        token2 = "second_token"

        monkeypatch.setenv("BITBUCKET_TOKEN", token1)
        result1 = get_token_from_envs()

        monkeypatch.setenv("BITBUCKET_TOKEN", token2)
        result2 = get_token_from_envs()

        assert result1 == token1
        assert result2 == token2
        assert result1 != result2
