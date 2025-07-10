
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import DiseaseStatistics, TrendAnalysis, RegionalData
from .serializers import DiseaseStatisticsSerializer, TrendAnalysisSerializer, RegionalDataSerializer
from diagnosis.models import DiagnosisRequest


class AnalyticsDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get user's diagnosis statistics
        user_diagnoses = DiagnosisRequest.objects.filter(user=request.user)
        
        # Recent trends (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_diagnoses = user_diagnoses.filter(created_at__gte=thirty_days_ago)
        
        stats = {
            'total_diagnoses': user_diagnoses.count(),
            'recent_diagnoses': recent_diagnoses.count(),
            'completed_diagnoses': user_diagnoses.filter(status='completed').count(),
            'pending_diagnoses': user_diagnoses.filter(status='pending').count(),
        }
        
        return Response(stats)


class DiseaseTrendsAPIView(generics.ListAPIView):
    serializer_class = DiseaseStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DiseaseStatistics.objects.all()
        
        # Filter by date range if provided
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        region = self.request.query_params.get('region')
        
        if year:
            queryset = queryset.filter(year=year)
        if month:
            queryset = queryset.filter(month=month)
        if region:
            queryset = queryset.filter(region__icontains=region)
        
        return queryset.order_by('-year', '-month')


class RegionalDataAPIView(generics.ListAPIView):
    queryset = RegionalData.objects.all()
    serializer_class = RegionalDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserActivityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get user activity data
        user_diagnoses = DiagnosisRequest.objects.filter(user=request.user)
        
        # Group by month for the last 12 months
        activity_data = []
        for i in range(12):
            month_start = timezone.now().replace(day=1) - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            
            count = user_diagnoses.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            
            activity_data.append({
                'month': month_start.strftime('%Y-%m'),
                'diagnoses': count
            })
        
        return Response(activity_data)
