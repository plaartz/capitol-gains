**Research Report**

**API Endpoint Calling and Filter Implementation in React**

**Summary of Work**  
I reviewed practical methods for API calling and filter management in React, specifically for implementing a search tool with pagination and dynamic filters. The main learning source was an interactive discussion with practical examples. I also reviewed articles on React API integration and Django-React connection through the Django REST Framework. These resources provided foundational knowledge on building search and filtering functionality in a frontend application.

**Motivation**  
The purpose of this research is to develop a search and filtering tool for our transaction data page, allowing users to view data based on custom filters. This capability enhances the user experience by supporting data-driven navigation and relates to Project Issue #40 on our project board.

**Time Spent**  
Total time: 75 minutes of research and hands-on examples, with an additional 15 minutes writing this report.

**Results**  

1. **React API Call Function**  
   We created a reusable API function in React (e.g., `search`) that accepts pagination and sorting parameters (`pageNo`, `pageSize`, `orderBy`) for flexible and efficient data querying.

2. **Context API for Filter Management**  
   Using React's Context API (e.g., `FilterContext`) provides centralized control of search filters, helping synchronize parameters across components and simplifying the code structure.

3. **Table Component for Data Display**  
   Implementing a responsive `Table` component allows for dynamic data sorting and pagination, controlled by a configurable `colOrder` object for easy updates to column structure.

4. **Pagination and UI**  
   Adding pagination controls directly within the `Table` component enables smooth navigation across data pages without reloading, updating `pageNo` and `pageSize` as needed.

5. **Django Backend API**  
   We structured a Django view (e.g., `search_view`) to validate incoming requests, ensuring that only valid data is processed, and provide paginated responses that match frontend requests.

6. **Scoped Component Styling**  
   Utilizing CSS modules like `Table.module.css` allows for isolated component styles, keeping layout changes contained and preventing style conflicts.

7. **Debugging and Data Validation**  
   During development, using `console.log()` statements and mock data ensures correct data flow, while testing various parameter combinations confirms accurate frontend updates.

**Sources**  
1. [Builtin on React API Integration](https://builtin.com/software-engineering-perspectives/react-api)  
2. [GeeksforGeeks Django-React Integration](https://www.geeksforgeeks.org/integrating-django-with-reactjs-using-django-rest-framework/)  
3. [ChatGPT Discussion Link](https://chatgpt.com/share/6722fbad-b624-8006-97c3-77ba2f1a7dd6)