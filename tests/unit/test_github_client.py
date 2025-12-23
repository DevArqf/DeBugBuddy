import pytest
from unittest.mock import Mock, patch, MagicMock
from debugbuddy.integrations.github.client import GitHubClient
from debugbuddy.integrations.github.search import GitHubSearcher
from debugbuddy.integrations.github.issues import IssueManager

class TestGitHubClient:

    def test_init_without_token(self):
        client = GitHubClient()

        assert client.token is None
        assert client.base_url == "https://api.github.com"
        assert "Accept" in client.headers
        assert "Authorization" not in client.headers

    def test_init_with_token(self):
        token = "test_token_123"
        client = GitHubClient(token=token)

        assert client.token == token
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == f"token {token}"

    @patch('requests.get')
    def test_search_issues_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'items': [
                {
                    'title': 'NameError in Python',
                    'html_url': 'https://github.com/user/repo/issues/1',
                    'state': 'open'
                }
            ]
        }
        mock_get.return_value = mock_response

        client = GitHubClient()
        results = client.search_issues('NameError', 'python')

        assert len(results) == 1
        assert results[0]['title'] == 'NameError in Python'
        assert results[0]['state'] == 'open'

    @patch('requests.get')
    def test_search_issues_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = GitHubClient()
        results = client.search_issues('NameError', 'python')

        assert results == []

    @patch('requests.post')
    def test_create_issue_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            'html_url': 'https://github.com/user/repo/issues/1',
            'number': 1,
            'title': 'Test Issue'
        }
        mock_post.return_value = mock_response

        client = GitHubClient(token='test_token')
        issue = client.create_issue(
            'user/repo',
            'Test Issue',
            'Test body',
            ['bug']
        )

        assert issue['number'] == 1
        assert issue['title'] == 'Test Issue'

    @patch('requests.post')
    def test_create_issue_with_labels(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'number': 1}
        mock_post.return_value = mock_response

        client = GitHubClient(token='test_token')
        labels = ['bug', 'debugbuddy', 'help-wanted']

        client.create_issue('user/repo', 'Title', 'Body', labels)

        call_args = mock_post.call_args
        assert call_args[1]['json']['labels'] == labels

class TestGitHubSearcher:

    def test_init(self):
        client = GitHubClient()
        searcher = GitHubSearcher(client)

        assert searcher.client == client

    @patch.object(GitHubClient, 'search_issues')
    def test_find_solutions(self, mock_search):
        mock_search.return_value = [
            {
                'title': 'Fix NameError',
                'html_url': 'https://github.com/user/repo/issues/1',
                'state': 'closed',
                'reactions': {'total_count': 10},
                'comments': 5
            },
            {
                'title': 'NameError help',
                'html_url': 'https://github.com/user/repo/issues/2',
                'state': 'open',
                'reactions': {'total_count': 3},
                'comments': 2
            }
        ]

        client = GitHubClient()
        searcher = GitHubSearcher(client)

        solutions = searcher.find_solutions('NameError', 'python', limit=2)

        assert len(solutions) == 2
        assert solutions[0]['title'] == 'Fix NameError'
        assert solutions[0]['reactions'] == 10
        assert solutions[0]['comments'] == 5

    @patch.object(GitHubClient, 'search_issues')
    def test_find_solutions_with_limit(self, mock_search):
        mock_search.return_value = [
            {'title': f'Issue {i}', 'html_url': f'url{i}', 'state': 'open',
             'reactions': {'total_count': 0}, 'comments': 0}
            for i in range(10)
        ]

        client = GitHubClient()
        searcher = GitHubSearcher(client)

        solutions = searcher.find_solutions('Error', 'python', limit=3)

        assert len(solutions) == 3

    @patch.object(GitHubClient, 'search_issues')
    def test_find_solutions_empty_results(self, mock_search):
        mock_search.return_value = []

        client = GitHubClient()
        searcher = GitHubSearcher(client)

        solutions = searcher.find_solutions('UnknownError', 'python')

        assert solutions == []

class TestIssueManager:

    def test_init(self):
        client = GitHubClient()
        manager = IssueManager(client)

        assert manager.client == client

    @patch('requests.get')
    def test_list_issues_open(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'number': 1, 'state': 'open', 'title': 'Bug'},
            {'number': 2, 'state': 'open', 'title': 'Feature'}
        ]
        mock_get.return_value = mock_response

        client = GitHubClient()
        manager = IssueManager(client)

        import requests as req
        with patch.object(req, 'get', mock_get):
            issues = manager.list_issues('user/repo', state='open')

        assert len(issues) == 2
        assert all(issue['state'] == 'open' for issue in issues)

    @patch('requests.get')
    def test_list_issues_closed(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'number': 3, 'state': 'closed', 'title': 'Fixed bug'}
        ]
        mock_get.return_value = mock_response

        client = GitHubClient()
        manager = IssueManager(client)

        import requests as req
        with patch.object(req, 'get', mock_get):
            issues = manager.list_issues('user/repo', state='closed')

        assert len(issues) == 1
        assert issues[0]['state'] == 'closed'

class TestGitHubIntegration:

    @patch('requests.get')
    @patch('requests.post')
    def test_search_and_create_workflow(self, mock_post, mock_get):
        search_response = Mock()
        search_response.status_code = 200
        search_response.json.return_value = {'items': []}
        mock_get.return_value = search_response

        create_response = Mock()
        create_response.json.return_value = {
            'number': 1,
            'html_url': 'https://github.com/user/repo/issues/1'
        }
        mock_post.return_value = create_response

        client = GitHubClient(token='test_token')
        searcher = GitHubSearcher(client)
        solutions = searcher.find_solutions('RareError', 'python')

        if not solutions:
            issue = client.create_issue(
                'user/repo',
                '[DeBugBuddy] RareError',
                'Error details here',
                ['bug', 'debugbuddy']
            )
            assert issue['number'] == 1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])