import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const ProcessList = () => {
    const [processes, setProcesses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [sortBy, setSortBy] = useState('name');
    const [sortOrder, setSortOrder] = useState('asc');
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    useEffect(() => {
        const fetchProcesses = async () => {
            try {
                setLoading(true);
                const response = await api.getProcesses(); // 페이지 및 검색 파라미터 제거
                console.log('API Response:', response);
                if (response && Array.isArray(response)) {
                    setProcesses(response);
                    setTotalPages(Math.ceil(response.length / pageSize));
                } else {
                    setProcesses([]);
                    setTotalPages(1);
                    setMessage('No processes available.');
                }
            } catch (error) {
                console.error('Error fetching processes:', error);
                setError(`Failed to fetch processes: ${error.message}`);
            } finally {
                setLoading(false);
            }
        };

        fetchProcesses();
    }, [page, pageSize, searchTerm, sortBy, sortOrder]);

    const handleDelete = async (id, name) => {
        if (window.confirm(`Are you sure you want to delete the process "${name}"?`)) {
            try {
                await api.deleteProcess(id);
                setMessage(`Process "${name}" has been successfully deleted.`);
                setPage(1);
            } catch (error) {
                console.error('Error deleting process:', error);
                setError(`Failed to delete process: ${error.message}`);
            }
        }
    };

    const handleExecute = async (id, name) => {
        try {
            await api.executeProcess(id);
            setMessage(`Process "${name}" has been successfully executed.`);
        } catch (error) {
            console.error('Error executing process:', error);
            setError(`Failed to execute process: ${error.message}`);
        }
    };

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
        setPage(1);
    };

    const handleSort = (field) => {
        if (field === sortBy) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortBy(field);
            setSortOrder('asc');
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="process-list">
            <h2>Process List</h2>
            {message && <div className="message">{message}</div>}
            <div className="controls">
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search processes..."
                        value={searchTerm}
                        onChange={handleSearch}
                    />
                </div>
                <div className="sort-controls">
                    <button onClick={() => handleSort('name')}>
                        Sort by Name {sortBy === 'name' && (sortOrder === 'asc' ? '▲' : '▼')}
                    </button>
                    <button onClick={() => handleSort('createdAt')}>
                        Sort by Date {sortBy === 'createdAt' && (sortOrder === 'asc' ? '▲' : '▼')}
                    </button>
                </div>
                <div className="page-size-control">
                    <label>
                        Page Size:
                        <select value={pageSize} onChange={(e) => setPageSize(Number(e.target.value))}>
                            <option value={5}>5</option>
                            <option value={10}>10</option>
                            <option value={20}>20</option>
                        </select>
                    </label>
                </div>
            </div>
            {processes.length === 0 ? (
                <p>No processes found.</p>
            ) : (
                <>
                    <ul>
                        {processes.map((process) => (
                            <li key={process.id}>
                                <div className="process-info">
                                    <Link to={`/process/${process.id}`} className="process-link">
                                        {process.name}
                                    </Link>
                                    <p className="process-description">{process.description}</p>
                                </div>
                                <div className="button-group">
                                    <Link to={`/process/${process.id}`} className="view-btn">
                                        View
                                    </Link>
                                    <button
                                        onClick={() => handleExecute(process.id, process.name)}
                                        className="execute-btn"
                                    >
                                        Execute
                                    </button>
                                    <button
                                        onClick={() => handleDelete(process.id, process.name)}
                                        className="delete-btn"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </li>
                        ))}
                    </ul>
                    <div className="pagination">
                        <button
                            onClick={() => setPage(Math.max(1, page - 1))}
                            disabled={page === 1}
                        >
                            Previous
                        </button>
                        <span>Page {page} of {totalPages}</span>
                        <button
                            onClick={() => setPage(Math.min(totalPages, page + 1))}
                            disabled={page === totalPages}
                        >
                            Next
                        </button>
                    </div>
                </>
            )}
            <Link to="/create" className="create-btn">
                Create New Process
            </Link>
        </div>
    );
};

export default ProcessList;
