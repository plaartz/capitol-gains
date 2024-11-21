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
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            tabIndex={currPageNo === 1 ? "-1" : "0"}
            aria-disabled={currPageNo === 1 ? "true" : "false"}
            onClick={() => paginate(currPageNo - 1)}
          >
            Prev
          </a>
        </li>

        {/* First Page */}
        <li
          className={`page-item ${currPageNo === 1 ? "active" : ""}`}
        >
          <a
            onClick={() => paginate(1)}
            href="#"
            className="page-link"
          >
            1
          </a>
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
            <a
              onClick={() => paginate(number)}
              href="#"
              className="page-link"
            >
              {number}
            </a>
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
          <li
            className={`page-item ${currPageNo === totalPages ? "active" : ""}`}
          >
            <a
              onClick={() => paginate(totalPages)}
              href="#"
              className="page-link"
            >
              {totalPages}
            </a>
          </li>
        )}

        {/* Next Button */}
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            tabIndex={currPageNo === totalPages ? "-1" : "0"}
            aria-disabled={currPageNo === totalPages ? "true" : "false"}
            onClick={() => paginate(currPageNo + 1)}
          >
            Next
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
