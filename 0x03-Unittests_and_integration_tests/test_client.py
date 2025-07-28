#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


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

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)
