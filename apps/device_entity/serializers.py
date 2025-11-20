from rest_framework import serializers
from apps.device_entity.models import DeviceEntityType

class DeviceEntityTypeSerializer(serializers.ModelSerializer):  
  class Meta: 
    model = DeviceEntityType
    fields = ["__all__"]
    
    
class DeviceEntitiesSerializer(serializers.ModelSerializer):
  class Meta: 
    model = DeviceEntityType
    fields = ["__all__"]