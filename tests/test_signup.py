import json 
from tests.BaseCase import BaseCase

class SignUpTest(BaseCase):

      
    def test_sucessful_signup(self):
        
        #Arrange  
        payload = json.dumps({
            "email": "ias_epf@hotmail.com",
            "password": "1234567"
        })
        
        #Act
        response = self.app.post('/api/auth/signup', 
                                 headers={"Content-Type": "application/json"}, data=payload)
        
        #Assert
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)
    
