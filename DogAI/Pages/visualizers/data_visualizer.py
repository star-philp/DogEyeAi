from typing import Protocol
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class DataVisualizer(Protocol):
    """인터페이스 분리 원칙(ISP)을 따르는 시각화 인터페이스"""
    
    def create_time_series(self, data: pd.DataFrame) -> go.Figure: ...
    def create_distribution(self, data: pd.DataFrame) -> go.Figure: ...

class PlotlyVisualizer:
    """Plotly 기반 시각화 구현"""
    
    def create_time_series(self, data: pd.DataFrame) -> go.Figure:
        """개선된 시계열 차트 생성"""
        time_series = data.copy()
        time_series['analysis_time'] = pd.to_datetime(time_series['analysis_time'])
        time_series = time_series.set_index('analysis_time').resample('D').size().reset_index()
        time_series.columns = ['analysis_time', 'count']
        
        fig = px.line(
            time_series,
            x='analysis_time',
            y='count',
            title='시간별 진단 횟수',
            labels={'analysis_time': '진단 날짜', 'count': '진단 횟수'}
        )
        
        fig.update_layout(
            hovermode='x unified',
            showlegend=True,
            xaxis_title="진단 날짜",
            yaxis_title="진단 횟수",
            font=dict(size=12),
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_distribution(self, data: pd.DataFrame) -> go.Figure:
        """개선된 분포 차트 생성"""
        class_dist = data['class'].value_counts().reset_index()
        class_dist.columns = ['class', 'count']
        
        fig = px.pie(
            class_dist,
            names='class',
            values='count',
            title='진단 결과 분포',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4  # 도넛 차트로 변경
        )
        
        fig.update_layout(
            showlegend=True,
            font=dict(size=12),
            annotations=[dict(text='전체 진단', x=0.5, y=0.5, font_size=12, showarrow=False)]
        )
        
        return fig 