// src/components/FinancialData.js

import React, { useState, useEffect, useRef } from 'react';
import { getFinancialData } from '../services/api'; // API 호출 함수
import { Table, Spinner, Form, Button, Pagination } from 'react-bootstrap';
import Chart from 'chart.js/auto';

const FinancialData = () => {
  const [financialData, setFinancialData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [companyName, setCompanyName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const limit = 10;

  const chartInstanceRef = useRef(null);
  const chartContainerRef = useRef(null);

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString('ko-KR', options);
  };

  const applyFilters = async () => {
    setLoading(true);
    setError(null);
    console.log('필터 적용:', { companyName, startDate, endDate, currentPage, limit });
    try {
      const response = await getFinancialData(companyName, startDate, endDate, currentPage, limit);
      if (response && response.data) {
        setFinancialData(response.data.data); // 새로운 데이터로 설정
        setTotalPages(Math.ceil(response.data.total / limit));
        console.log('API로부터 받은 데이터:', response.data.data);
      } else {
        setFinancialData([]);
        setTotalPages(1);
        console.warn('예상치 못한 API 응답 구조:', response);
      }
    } catch (error) {
      console.error('재무 데이터를 가져오는 중 오류 발생:', error);
      setError('서버에서 데이터를 가져오는 데 오류가 발생했습니다.');
      setFinancialData([]);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    applyFilters();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, companyName, startDate, endDate]); // 의존성 배열에 필터 변수 추가

  const renderPagination = () => {
    if (totalPages <= 1) return null;

    let items = [];
    for (let number = 1; number <= totalPages; number++) {
      items.push(
        <Pagination.Item
          key={number}
          active={number === currentPage}
          onClick={() => setCurrentPage(number)}
        >
          {number}
        </Pagination.Item>
      );
    }
    return <Pagination>{items}</Pagination>;
  };

  useEffect(() => {
    if (financialData.length > 0) {
      const ctx = chartContainerRef.current.getContext('2d');

      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }

      chartInstanceRef.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: financialData.map((item) => formatDate(item.period_start)),
          datasets: [
            {
              label: '총 수익',
              data: financialData.map((item) => item.total_revenue),
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
            },
            {
              label: '순이익',
              data: financialData.map((item) => item.net_income),
              borderColor: 'rgba(153, 102, 255, 1)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
            },
          ],
        },
        options: {
          scales: {
            y: { beginAtZero: true },
          },
        },
      });
    } else {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    }

    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
        chartInstanceRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [financialData]);

  return (
    <div style={{ padding: '20px' }}>
      <h2>재무 데이터 개요</h2>
      <Form>
        <Form.Group controlId="companyName">
          <Form.Label>회사 이름</Form.Label>
          <Form.Control
            type="text"
            placeholder="회사 이름을 입력하세요"
            value={companyName}
            onChange={(e) => {
              setCompanyName(e.target.value);
              console.log('회사 이름 업데이트:', e.target.value);
            }}
          />
        </Form.Group>
        <Form.Group controlId="startDate">
          <Form.Label>시작 날짜</Form.Label>
          <Form.Control
            type="date"
            value={startDate}
            onChange={(e) => {
              setStartDate(e.target.value);
              console.log('시작 날짜 업데이트:', e.target.value);
            }}
          />
        </Form.Group>
        <Form.Group controlId="endDate">
          <Form.Label>종료일</Form.Label>
          <Form.Control
            type="date"
            value={endDate}
            onChange={(e) => {
              setEndDate(e.target.value);
              console.log('종료일 업데이트:', e.target.value);
            }}
          />
        </Form.Group>
        <Button
          variant="primary"
          onClick={() => {
            setCurrentPage(1);
            applyFilters();
            console.log('필터 적용 버튼 클릭됨');
          }}
          style={{ marginTop: '10px' }}
        >
          필터 적용
        </Button>
      </Form>

      {/* 적용된 필터 표시 */}
      <div style={{ marginTop: '20px' }}>
        <h3>적용된 필터</h3>
        <p>
          <strong>회사 이름: </strong>{companyName.trim() !== '' ? companyName : '전체'}
        </p>
        <p>
          <strong>시작 날짜: </strong>{startDate ? formatDate(startDate) : '전체'}
        </p>
        <p>
          <strong>종료일: </strong>{endDate ? formatDate(endDate) : '전체'}
        </p>
      </div>

      {/* 로딩 스피너 */}
      {loading && (
        <div style={{ marginTop: '20px' }}>
          <Spinner animation="border" />
        </div>
      )}

      {/* 에러 메시지 */}
      {error && (
        <div style={{ marginTop: '20px', color: 'red' }}>
          <p>{error}</p>
        </div>
      )}

      {/* 데이터 테이블 및 차트 */}
      {!loading && !error && financialData.length > 0 && (
        <>
          <Table striped bordered hover style={{ marginTop: '20px' }}>
            <thead>
              <tr>
                <th>회사 이름</th>
                <th>보고서 유형</th>
                <th>총 수익</th>
                <th>순이익</th>
                <th>기간 시작</th>
                <th>기간 종료</th>
              </tr>
            </thead>
            <tbody>
              {financialData.map((item) => (
                <tr key={item.id}> {/* 고유한 id를 key로 사용 */}
                  <td>{item.company_name}</td>
                  <td>{item.report_type}</td>
                  <td>{item.total_revenue.toLocaleString()} 원</td>
                  <td>{item.net_income.toLocaleString()} 원</td>
                  <td>{formatDate(item.period_start)}</td>
                  <td>{formatDate(item.period_end)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
          <div style={{ marginTop: '20px' }}>
            <canvas ref={chartContainerRef} width="400" height="200"></canvas>
          </div>
          {renderPagination()}
        </>
      )}

      {/* 데이터가 없을 경우 표시 */}
      {!loading && !error && financialData.length === 0 && (
        <div style={{ marginTop: '20px' }}>
          <p>재무 데이터를 찾을 수 없습니다.</p>
        </div>
      )}
    </div>
  );
};

export default FinancialData;
