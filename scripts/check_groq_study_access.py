"""One provider access check, charged to the shared campaign ledger."""
from pathlib import Path
from study_groq_client import StudyClient

client = StudyClient(Path('research/groq_study_20261118/api'), max_tokens=64)
response = client.call([{'role': 'user', 'content': 'Reply only OK.'}],
                       seed=42, label='infrastructure_access_check')
print({'http_status': response.get('http_status'),
       'finish_reason': response['finish_reason'],
       'content_received': bool(response['content']),
       'conservative_total_usd': client.spent_usd})
