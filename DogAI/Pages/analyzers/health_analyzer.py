from dataclasses import dataclass
from typing import List, Dict, Optional
import numpy as np

@dataclass
class AnalysisResult:
    diagnosis: str
    confidence: float
    recommendations: List[str]
    severity_level: int

class HealthAnalyzer:
    """단일 책임 원칙(SRP)을 따르는 건강 분석 클래스"""
    
    def analyze(self, pred_class: str, probs: np.ndarray) -> AnalysisResult:
        confidence = float(probs.max()) * 100
        severity = self._calculate_severity(confidence)
        recommendations = self._get_recommendations(pred_class, severity)
        
        return AnalysisResult(
            diagnosis=pred_class,
            confidence=confidence,
            recommendations=recommendations,
            severity_level=severity
        )
    
    def _calculate_severity(self, confidence: float) -> int:
        return min(max(int(confidence / 10), 1), 10)
    
    def _get_recommendations(self, pred_class: str, severity: int) -> List[str]:
        if pred_class == "Positive":
            return [
                "24시간 이내 수의사 상담 권장",
                "반려견의 눈 주변을 만지지 말 것",
                "깨끗한 환경 유지"
            ]
        return [
            "정기적인 눈 건강 체크 권장",
            "예방을 위한 위생 관리 지속"
        ]

    def _get_severity_text(self, confidence: float, pred_class: str) -> str:
        """신뢰도와 예측 클래스에 따른 맞춤형 심각도 메시지 반환"""
        level = self._calculate_severity(confidence)
        
        if pred_class == "Positive":
            messages = {
                1: "초기 염증 징후: 주의 깊은 관찰이 필요합니다.",
                2: "경미한 염증: 정기적인 관찰을 권장합니다.",
                3: "중등도 염증: 수의사 상담을 고려하세요.",
                4: "진행성 염증: 48시간 내 수의사 상담 권장.",
                5: "심각한 염증: 24시간 내 수의사 진료 필요.",
                6: "매우 심각한 염증: 즉시 수의사 진료가 필요합니다.",
                7: "위험한 상태: 응급 진료가 필요합니다.",
                8: "매우 위험: 즉시 응급 진료소로 이동하세요.",
                9: "극도로 위험: 즉각적인 치료가 필요합니다.",
                10: "생명이 위험한 상태: 즉시 응급 처치가 필요합니다."
            }
        else:
            messages = {
                1: "매우 건강한 상태: 정기적인 관리를 유지하세요.",
                2: "건강한 상태: 현재 관리 상태를 유지하세요.",
                3: "양호한 상태: 주기적인 검진을 권장합니다.",
                4: "관찰 필요: 변화가 있는지 주의 깊게 지켜보세요.",
                5: "예방 관리 필요: 정기적인 검진을 받으세요.",
                6: "주의 필요: 수의사 상담을 고려해보세요.",
                7: "검진 권장: 가까운 시일 내 검진을 받으세요.",
                8: "즉시 검진: 수의사 검진을 받으세요.",
                9: "진료 필요: 빠른 시일 내 진료가 필요합니다.",
                10: "즉시 진료: 수의사의 진단이 필요합니다."
            }
        
        return messages.get(level, "알 수 없는 상태") 