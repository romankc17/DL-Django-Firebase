from clients import Client
import initialize
import unittest

initialize.initialize()

class TestClient(unittest.TestCase):

    def test_clients_number(self):
        limit = 50
        client = Client()
        c=client.getNClients(limit=limit)
        self.assertEqual (len(c['docs']) , limit, "Should be 10")
        
    def test_last_doc(self):
        client = Client()
        cs,l=client.getNClients(limit=40)
        last_doc = cs[-1].id
        last_doc_clientAddedAt = last_doc['clientAddedAt']
        self.assertEqual (last_doc_clientAddedAt , c['last_doc_clientAddedAt'])
    
    
if __name__ == '__main__':
    unittest.main()
    
