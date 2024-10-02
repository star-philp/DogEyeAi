// src/services/api.js

import axios from 'axios';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // FastAPI 서버 주소
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 재무 데이터 가져오기
 * @param {string} companyName - 회사 이름
 * @param {string} startDate - 시작 날짜 (YYYY-MM-DD)
 * @param {string} endDate - 종료 날짜 (YYYY-MM-DD)
 * @param {number} page - 페이지 번호
 * @param {number} limit - 페이지당 데이터 수
 * @returns {Promise} - Axios 응답 프로미스
 */
export const getFinancialData = (companyName, startDate, endDate, page, limit) => {
  const params = {};
  if (companyName.trim() !== '') params.company_name = companyName.trim();
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  if (page) params.page = page;
  if (limit) params.limit = limit;

  return apiClient.get('/financial_data/', { params });
};
