from rest_framework import serializers
from .models import Goods, Images, Parameters


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['file', 'sign']


class ParametersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameters
        fields = ['name', 'value', 'cost']


class GoodsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    parameters = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = ['name', 'info', 'base_cost', 'images', 'parameters']

    def get_images(self, obj):
        if self.context.get('request').parser_context['kwargs'].get('pk'):
            return ImagesSerializer(obj.images.all(), many=True).data
        return None

    def get_parameters(self, obj):
        if self.context.get('request').parser_context['kwargs'].get('pk'):
            return ParametersSerializer(obj.parameters.all(), many=True).data
        return None

    def to_representation(self, instance) -> dict:
        """
        Remove all dict pairs with None values for exclude fields
        with no real values.

        :param instance:
        :return: dict
        """
        data = super().to_representation(instance)
        clean_dict = {key: value for key, value in data.items() if value is not None}
        return clean_dict
