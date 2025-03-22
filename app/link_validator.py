import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional, Dict, Tuple
from .exceptions import InvalidURLError, UnsafeURLError, InvalidAliasError

class LinkValidator:
    # List of unsafe URL patterns
    UNSAFE_PATTERNS = [
        r'\.(exe|dll|bat|cmd|ps1|vbs|js|jar|war|zip|rar|7z)$',
        r'\.(php|asp|jsp|cgi|pl|py|rb|sh)$',
        r'\.(bin|dat|db|sql|sqlite|mdb)$',
        r'\.(dmg|iso|img|vhd|vmdk)$',
        r'\.(pkg|msi|msm|msp)$',
        r'\.(swf|fla|flv|f4v|f4p|f4a|f4b)$',
        r'\.(class|ear|war|sar|nar)$',
        r'\.(bak|tmp|temp|cache|log)$',
        r'\.(config|conf|ini|cfg|xml|json|yaml|yml)$',
        r'\.(key|pem|cert|crt|der|p12|pfx)$',
        r'\.(env|env.*|.env|.env.*)$',
        r'\.(git|svn|hg|bzr|cvs)$',
        r'\.(lock|pid|sock|pipe|fifo)$',
        r'\.(core|dump|crash|error|fail)$',
        r'\.(backup|restore|recovery|revert)$',
        r'\.(install|setup|uninstall|remove)$',
        r'\.(update|upgrade|patch|fix)$',
        r'\.(debug|test|dev|staging|prod)$',
        r'\.(local|localhost|127\.0\.0\.1)$',
        r'\.(internal|private|secret|hidden)$',
        r'\.(admin|administrator|root|superuser)$',
        r'\.(system|service|daemon|worker)$',
        r'\.(api|rest|graphql|soap|rpc)$',
        r'\.(auth|login|signin|register|signup)$',
        r'\.(password|secret|token|key|credential)$',
        r'\.(session|cookie|cache|storage)$',
        r'\.(upload|download|transfer|share)$',
        r'\.(execute|run|start|stop|restart)$',
        r'\.(shell|terminal|console|command)$',
        r'\.(script|program|application|app)$',
        r'\.(process|thread|job|task)$',
        r'\.(memory|disk|storage|cache)$',
        r'\.(network|socket|port|connection)$',
        r'\.(security|firewall|antivirus|malware)$',
        r'\.(backup|restore|recovery|revert)$',
        r'\.(install|setup|uninstall|remove)$',
        r'\.(update|upgrade|patch|fix)$',
        r'\.(debug|test|dev|staging|prod)$',
        r'\.(local|localhost|127\.0\.0\.1)$',
        r'\.(internal|private|secret|hidden)$',
        r'\.(admin|administrator|root|superuser)$',
        r'\.(system|service|daemon|worker)$',
        r'\.(api|rest|graphql|soap|rpc)$',
        r'\.(auth|login|signin|register|signup)$',
        r'\.(password|secret|token|key|credential)$',
        r'\.(session|cookie|cache|storage)$',
        r'\.(upload|download|transfer|share)$',
        r'\.(execute|run|start|stop|restart)$',
        r'\.(shell|terminal|console|command)$',
        r'\.(script|program|application|app)$',
        r'\.(process|thread|job|task)$',
        r'\.(memory|disk|storage|cache)$',
        r'\.(network|socket|port|connection)$',
        r'\.(security|firewall|antivirus|malware)$',
    ]

    # List of safe file extensions
    SAFE_EXTENSIONS = {
        '.html', '.htm', '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt',
        '.csv', '.xml', '.json', '.yaml', '.yml', '.md', '.markdown'
    }

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if the URL is properly formatted."""
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise InvalidURLError("URL must include scheme (http:// or https://) and domain")
            return True
        except Exception as e:
            raise InvalidURLError(f"Invalid URL format: {str(e)}")

    @staticmethod
    def is_safe_url(url: str) -> bool:
        """Check if the URL is safe to process."""
        # Check URL format
        if not LinkValidator.validate_url(url):
            raise InvalidURLError("Invalid URL format")

        # Check for unsafe patterns
        for pattern in LinkValidator.UNSAFE_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                raise UnsafeURLError(f"URL contains unsafe pattern: {pattern}")

        # Check file extension
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        if any(path.endswith(ext) for ext in LinkValidator.SAFE_EXTENSIONS):
            return True

        # If no extension or not in safe list, check content type
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            content_type = response.headers.get('content-type', '').lower()
            
            # Check if content type is safe
            safe_content_types = {
                'text/html', 'text/plain', 'text/css', 'text/javascript',
                'application/javascript', 'application/json', 'application/xml',
                'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml',
                'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
            }
            
            return any(safe_type in content_type for safe_type in safe_content_types)
        except Exception:
            return False

    @staticmethod
    def validate_alias(alias: str) -> bool:
        """Validate custom alias format."""
        # Alias should be 3-50 characters long
        if not (3 <= len(alias) <= 50):
            raise InvalidAliasError("Alias must be between 3 and 50 characters")

        # Alias should only contain alphanumeric characters, hyphens, and underscores
        if not re.match(r'^[a-zA-Z0-9_-]+$', alias):
            raise InvalidAliasError("Alias can only contain letters, numbers, hyphens, and underscores")

        # Alias should not start or end with a hyphen or underscore
        if alias[0] in '-_' or alias[-1] in '-_':
            raise InvalidAliasError("Alias cannot start or end with a hyphen or underscore")

        return True

    @staticmethod
    def generate_preview(url: str) -> Dict[str, str]:
        """Generate preview information for a URL."""
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else ''
            
            # Extract description
            description = ''
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            elif soup.find('meta', attrs={'property': 'og:description'}):
                description = soup.find('meta', attrs={'property': 'og:description'}).get('content', '')
            
            # Extract image
            image = ''
            og_image = soup.find('meta', attrs={'property': 'og:image'})
            if og_image:
                image = og_image.get('content', '')
            elif soup.find('meta', attrs={'name': 'twitter:image'}):
                image = soup.find('meta', attrs={'name': 'twitter:image'}).get('content', '')
            
            return {
                'title': title.strip(),
                'description': description.strip(),
                'image': image.strip()
            }
        except Exception:
            return {
                'title': '',
                'description': '',
                'image': ''
            } 