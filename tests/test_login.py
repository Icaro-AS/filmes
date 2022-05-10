import json 
from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):
    
    def test_sucessful_login(self):
        
        #Arrange
        email = "ias_epf@hotmail.com"
        password = "1234567"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        
        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)
        
        #Act
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=payload)
        
        #Assert
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)