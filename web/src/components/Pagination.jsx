const Pagination = ({ totalPosts, pageSize, currPageNo, paginate }) => {
  const pageNo = [];
  var lastPage = Math.ceil(totalPosts / pageSize);

  console.log(currPageNo);

  const totalPages = Math.ceil(totalPosts / pageSize);
  const maxVisiblePages = 5;
  const endDeck = (Math.floor((totalPages - 1)/maxVisiblePages)) * maxVisiblePages + 1

  // Calculate the start and end of the current range
  const startPage = Math.floor((currPageNo - 1) / maxVisiblePages) * maxVisiblePages + 1;
  const endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

  console.log(`starPage = ${startPage} endDeck = ${endDeck}`)

  // Generate page numbers for the current range
  for (let i = startPage; i <= endPage; i++) {
    pageNo.push(i);
  }

  return (
    <nav>
      <ul className="pagination justify-content-center">
        <li className="page-item">
          <a
          className="page-link"
          href="#"
          tabIndex={startPage === 1 ? "-1" : "0"}
          aria-disabled={startPage === 1 ? "true" : "false"}
          onClick={() => paginate(startPage - 1)}
          >
            Prev Grp
          </a>
        </li>
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
          <li
            key={numbers}
            className={`page-item ${currPageNo === numbers ? "active" : ""}`}
          >
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
        <li className="page-item">
        <a
          className="page-link"
          href="#"
          tabIndex={startPage === endDeck ? "-1" : "0"}
          aria-disabled={startPage === endDeck ? "true" : "false"}
          onClick={() => paginate(endPage + 1)}
          >
            Next Grp
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Pagination;
