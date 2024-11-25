import { useEffect, useState } from "react";

const Pagination = ({ totalPosts, pageSize, currPageNo, paginate }) => {
  const [pageNo, setPageNo] = useState([]);
  const totalPages = Math.ceil(totalPosts / pageSize);
  const maxVisiblePages = 5;

  useEffect(() => {
    const generatePageNumbers = () => {
      const pages = [];
      const startPage = Math.max(
        2,
        Math.min(currPageNo - Math.floor(maxVisiblePages / 2), totalPages - maxVisiblePages + 1)
      );
      const endPage = Math.min(totalPages - 1, startPage + maxVisiblePages - 1);

      // Add the pages to display
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      setPageNo(pages);
    };

    generatePageNumbers();
  }, [currPageNo, totalPages]);

  return (
    <nav>
      <ul className="pagination justify-content-center">
        {/* Previous Button */}
        <li className={`page-item ${currPageNo === 1 ? "disabled" : ""}`}>
          <button
            className="page-link"
            disabled={currPageNo === 1}
            onClick={() => paginate(currPageNo - 1)}
          >
            Prev
          </button>
        </li>

        {/* First Page */}
        <li className={`page-item ${currPageNo === 1 ? "active" : ""}`}>
          <button onClick={() => paginate(1)} className="page-link">
            1
          </button>
        </li>

        {/* Ellipsis for Pages Before */}
        {pageNo[0] > 2 && (
          <li className="page-item disabled">
            <span className="page-link">...</span>
          </li>
        )}

        {/* Dynamic Pages */}
        {pageNo.map((number) => (
          <li
            key={number}
            className={`page-item ${currPageNo === number ? "active" : ""}`}
          >
            <button onClick={() => paginate(number)} className="page-link">
              {number}
            </button>
          </li>
        ))}

        {/* Ellipsis for Pages After */}
        {pageNo[pageNo.length - 1] < totalPages - 1 && (
          <li className="page-item disabled">
            <span className="page-link">...</span>
          </li>
        )}

        {/* Last Page */}
        {totalPages > 1 && (
          <li className={`page-item ${currPageNo === totalPages ? "active" : ""}`}>
            <button onClick={() => paginate(totalPages)} className="page-link">
              {totalPages}
            </button>
          </li>
        )}

        {/* Next Button */}
        <li className={`page-item ${currPageNo === totalPages ? "disabled" : ""}`}>
          <button
            className="page-link"
            disabled={currPageNo === totalPages}
            onClick={() => paginate(currPageNo + 1)}
          >
            Next
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
