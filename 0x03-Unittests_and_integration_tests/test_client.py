#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Test the GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct result"""
        expected = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org  # This accesses the memoized method

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test _public_repos_url with mocked org payload"""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }

            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of names"""
        test_payload = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache-2.0"}},
            {"name": "repo3", "license": {"key": "MIT"}},
        ]

        mock_get_json.return_value = test_payload

        with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/test_org/repos"
            )

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
