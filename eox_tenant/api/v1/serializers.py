"""
Serializers file for eox_tenant api v1.
"""
from rest_framework import serializers

from eox_tenant.models import Microsite, Route, TenantConfig


class MicrositeSerializer(serializers.ModelSerializer):
    """Serializer class for Microsite model."""

    values = serializers.JSONField()

    class Meta:
        """Define the serializer fields."""

        model = Microsite
        fields = '__all__'


class TenantConfigSerializer(serializers.ModelSerializer):
    """Serializer class for TenantConfig model."""

    lms_configs = serializers.JSONField()
    studio_configs = serializers.JSONField()
    theming_configs = serializers.JSONField()
    meta = serializers.JSONField()

    class Meta:
        """Define the serializer fields."""

        model = TenantConfig
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """Serializer class for Route model."""

    class Meta:
        """Define the serializer fields."""

        model = Route
        fields = '__all__'
