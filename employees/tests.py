from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee
from django.contrib.auth.models import User

class EmployeeTests(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.token = response.data['access']  
        
        self.url = reverse('employee-list')  
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'department': 'Engineering',
            'role': 'Developer',
        }

    def test_create_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(self.url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'John Doe')

    def test_create_employee_with_duplicate_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(self.url, self.employee_data, format='json')
        response = self.client.post(self.url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_employees(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.post(self.url, self.employee_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.get(reverse('employee-detail', args=[employee.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], employee.name)

    def test_update_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        employee = Employee.objects.create(**self.employee_data)
        update_data = {'name': 'Jane Doe'}
        response = self.client.put(reverse('employee-detail', args=[employee.id]), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'Jane Doe')

    def test_delete_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        employee = Employee.objects.create(**self.employee_data)
        response = self.client.delete(reverse('employee-detail', args=[employee.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

