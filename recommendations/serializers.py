
from rest_framework import serializers
from .models import Recommendation, Treatment, TreatmentRecommendation, TreatmentTracking


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = [
            'id', 'name', 'treatment_type', 'active_ingredients',
            'application_method', 'dosage_instructions', 'safety_precautions',
            'cost_estimate', 'effectiveness_rating', 'organic_friendly'
        ]


class TreatmentRecommendationSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)

    class Meta:
        model = TreatmentRecommendation
        fields = [
            'treatment', 'order', 'specific_instructions',
            'quantity_needed', 'application_frequency'
        ]


class RecommendationSerializer(serializers.ModelSerializer):
    treatment_recommendations = TreatmentRecommendationSerializer(
        source='treatmentrecommendation_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Recommendation
        fields = [
            'id', 'custom_recommendations', 'priority_level',
            'estimated_cost', 'timeline', 'follow_up_required',
            'follow_up_date', 'treatment_recommendations', 'created_at'
        ]


class TreatmentTrackingSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)

    class Meta:
        model = TreatmentTracking
        fields = [
            'id', 'treatment', 'status', 'start_date', 'completion_date',
            'notes', 'effectiveness_rating', 'side_effects_observed',
            'cost_incurred', 'created_at', 'updated_at'
        ]
