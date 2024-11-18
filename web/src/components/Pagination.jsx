import React from "react";
import styles from "./styles/Table.module.css";

const Pagination = ({ totalPosts, pageSize, currPageNo, paginate }) => {
  const pageNo = [];
  var lastPage = Math.ceil(totalPosts / pageSize);

  console.log(currPageNo);

  for (var i = 1; i <= lastPage; i++) {
    pageNo.push(i);
  }

  return (
    <nav>
      <ul className="pagination justify-content-center">
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            tabIndex={currPageNo === 1 ? "-1" : "0"}
            aria-disabled={currPageNo === 1 ? "true" : "false"}
            onClick={() => paginate(0)}
          >
            Prev
          </a>
        </li>
        {pageNo.map((numbers) => (
          <li key={numbers} className={`page-item ${currPageNo === numbers ? "active" : ""}`}>
            <a onClick={() => paginate(numbers)} href="#" className="page-link">
              {numbers}
            </a>
          </li>
        ))}
        <li className="page-item">
          <a
            className="page-link"
            href="#"
            tabIndex={currPageNo === lastPage ? "-1" : "0"}
            aria-disabled={currPageNo === lastPage ? "true" : "false"}
            onClick={() => paginate(-1)}
          >
            Next
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
