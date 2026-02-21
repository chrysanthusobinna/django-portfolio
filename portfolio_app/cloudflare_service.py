import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class CloudflareService:
    """Service for interacting with Cloudflare API"""
    
    def __init__(self):
        self.api_token = getattr(settings, 'CLOUDFLARE_API_TOKEN', None)
        self.account_id = getattr(settings, 'CLOUDFLARE_ACCOUNT_ID', None)
        self.base_url = 'https://api.cloudflare.com/client/v4'
        
        if not self.api_token:
            logger.warning("Cloudflare API token not configured")
    
    def _make_request(self, method, endpoint, data=None):
        """Make a request to Cloudflare API"""
        if not self.api_token:
            raise ValueError("Cloudflare API token not configured")
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Cloudflare API error: {e}")
            raise
    
    def add_domain(self, domain_name):
        """Add a domain to Cloudflare"""
        try:
            # First, add the domain to the account
            endpoint = '/zones'
            data = {
                'name': domain_name,
                'account': {
                    'id': self.account_id
                },
                'jump_start': True,
                'type': 'full'
            }
            
            result = self._make_request('POST', endpoint, data)
            
            if result.get('success'):
                zone_id = result['result']['id']
                logger.info(f"Successfully added domain {domain_name} to Cloudflare. Zone ID: {zone_id}")
                return {
                    'success': True,
                    'zone_id': zone_id,
                    'message': f'Domain {domain_name} added successfully to Cloudflare'
                }
            else:
                error_msg = result.get('errors', [{'message': 'Unknown error'}])[0]['message']
                logger.error(f"Failed to add domain to Cloudflare: {error_msg}")
                return {
                    'success': False,
                    'message': f'Failed to add domain to Cloudflare: {error_msg}'
                }
                
        except Exception as e:
            logger.error(f"Error adding domain to Cloudflare: {e}")
            return {
                'success': False,
                'message': f'Error adding domain to Cloudflare: {str(e)}'
            }
    
    def get_zone_info(self, domain_name):
        """Get zone information for a domain"""
        try:
            endpoint = f'/zones?name={domain_name}'
            result = self._make_request('GET', endpoint)
            
            if result.get('success') and result.get('result'):
                zone = result['result'][0]
                return {
                    'success': True,
                    'zone_id': zone['id'],
                    'status': zone['status'],
                    'name_servers': zone.get('name_servers', [])
                }
            else:
                return {
                    'success': False,
                    'message': 'Zone not found'
                }
        except Exception as e:
            logger.error(f"Error getting zone info: {e}")
            return {
                'success': False,
                'message': f'Error getting zone info: {str(e)}'
            }
    
    def get_dns_records(self, zone_id):
        """Get DNS records for a zone"""
        try:
            endpoint = f'/zones/{zone_id}/dns_records'
            result = self._make_request('GET', endpoint)
            
            if result.get('success'):
                records = result['result']
                # Filter for A and CNAME records that are relevant
                relevant_records = []
                for record in records:
                    if record['type'] in ['A', 'CNAME', 'NS']:
                        relevant_records.append({
                            'type': record['type'],
                            'name': record['name'],
                            'content': record['content'],
                            'ttl': record['ttl']
                        })
                return {
                    'success': True,
                    'records': relevant_records,
                    'name_servers': self.get_name_servers(zone_id)
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to get DNS records'
                }
        except Exception as e:
            logger.error(f"Error getting DNS records: {e}")
            return {
                'success': False,
                'message': f'Error getting DNS records: {str(e)}'
            }
    
    def get_name_servers(self, zone_id):
        """Get name servers for a zone"""
        try:
            endpoint = f'/zones/{zone_id}'
            result = self._make_request('GET', endpoint)
            
            if result.get('success'):
                return result['result'].get('name_servers', [])
            return []
        except Exception as e:
            logger.error(f"Error getting name servers: {e}")
            return []
    
    def delete_domain(self, domain_name):
        try:
            # First get the zone ID
            zone_info = self.get_zone_info(domain_name)
            if not zone_info['success']:
                return zone_info
            
            zone_id = zone_info['zone_id']
            endpoint = f'/zones/{zone_id}'
            
            result = self._make_request('DELETE', endpoint)
            
            if result.get('success'):
                logger.info(f"Successfully deleted domain {domain_name} from Cloudflare")
                return {
                    'success': True,
                    'message': f'Domain {domain_name} deleted successfully from Cloudflare'
                }
            else:
                error_msg = result.get('errors', [{'message': 'Unknown error'}])[0]['message']
                logger.error(f"Failed to delete domain from Cloudflare: {error_msg}")
                return {
                    'success': False,
                    'message': f'Failed to delete domain from Cloudflare: {error_msg}'
                }
                
        except Exception as e:
            logger.error(f"Error deleting domain from Cloudflare: {e}")
            return {
                'success': False,
                'message': f'Error deleting domain from Cloudflare: {str(e)}'
            }
