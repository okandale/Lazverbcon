import React from 'react';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const maxVisiblePages = 5;

  const getVisiblePages = () => {
    const pages = [];
    const half = Math.floor(maxVisiblePages / 2);

    let start = Math.max(1, currentPage - half);
    let end = Math.min(totalPages, start + maxVisiblePages - 1);

    if (end - start < maxVisiblePages - 1) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  };

  const visiblePages = getVisiblePages();

  return (
    <div className="flex gap-1 items-center justify-center">
      <button
        className="px-2 py-1 border rounded disabled:opacity-50"
        onClick={() => onPageChange(1)}
        disabled={currentPage === 1}
      >
        &laquo;
      </button>
      <button
        className="px-2 py-1 border rounded disabled:opacity-50"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
      >
        &lsaquo;
      </button>
      {visiblePages.map((page) => (
        <button
          key={page}
          className={`px-3 py-1 border rounded ${
            page === currentPage ? 'bg-blue-500 text-white' : ''
          }`}
          onClick={() => onPageChange(page)}
        >
          {page}
        </button>
      ))}
      <button
        className="px-2 py-1 border rounded disabled:opacity-50"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      >
        &rsaquo;
      </button>
      <button
        className="px-2 py-1 border rounded disabled:opacity-50"
        onClick={() => onPageChange(totalPages)}
        disabled={currentPage === totalPages}
      >
        &raquo;
      </button>
    </div>
  );
};

export default Pagination;
