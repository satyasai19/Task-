from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField()

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_email(self, value):
        
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        
        if '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_name(self, value):
        
        if not value or value.strip() == "":
            raise serializers.ValidationError("Name is required.")
        return value
        # if not serializer.is_valid():
        #     logger.error("Validation errors: %s", serializer.errors)
